"""LLM-driven self-modification workflow.

This module replaces the previous no-op stub with a small, usable
self-modification loop. When invoked it will:

1. Ask an LLM to generate a unified diff for the target files.
2. Apply the patch to the repository.
3. Run the test suite.
4. Commit the change if tests pass.

If no API key is configured the graph will bail out gracefully with a
``failed`` status so the rest of the project and its tests can still run
without external dependencies.
"""

from __future__ import annotations

import subprocess
import textwrap
from pathlib import Path
from typing import Literal, TypedDict

from config import SETTINGS
from llm import make_llm


class SelfModState(TypedDict):
    goal: str
    file_list: list[str]
    last_result: str
    status: Literal["start", "patched", "tested", "merged", "failed"]
    attempts: int


class _SelfModGraph:
    """Minimal self-modification state machine backed by an LLM."""

    def __init__(self) -> None:
        # Repo root is three levels up from this file: ``src/iea/graphs`` → project root
        self.repo_root = Path(__file__).resolve().parents[3]

    def _apply_patch(self, patch: str) -> tuple[bool, str]:
        """Apply a unified diff patch to the repository.

        Returns a tuple ``(success, output)`` where ``output`` contains any
        stdout/stderr from ``git apply``.
        """

        proc = subprocess.run(
            ["git", "apply", "--whitespace=nowarn", "-"],
            input=patch,
            text=True,
            capture_output=True,
            cwd=self.repo_root,
        )
        return proc.returncode == 0, proc.stdout + proc.stderr

    def invoke(self, state: SelfModState) -> SelfModState:  # pragma: no cover
        status = state["status"]

        if status == "start":
            # Ensure we have credentials to talk to an LLM
            if not (SETTINGS.openai_api_key or SETTINGS.openrouter_api_key):
                return {**state, "status": "failed", "last_result": "Missing API key"}

            llm = make_llm("code")
            files = "\n".join(f"- {f}" for f in state["file_list"])
            prompt = textwrap.dedent(
                f"""
                You are modifying a codebase. Goal: {state['goal']}
                Provide a unified diff patch for the following files:

                {files}

                Only output the patch.
                """
            )
            try:
                resp = llm.invoke(prompt)
            except Exception as exc:  # pragma: no cover - network errors
                return {**state, "status": "failed", "last_result": str(exc)}

            patch_text = resp.content if hasattr(resp, "content") else str(resp)
            ok, msg = self._apply_patch(patch_text)
            if not ok:
                return {**state, "status": "failed", "last_result": msg or patch_text}
            return {**state, "status": "patched", "last_result": patch_text}

        if status == "patched":
            proc = subprocess.run(
                ["pytest", "-q"],
                cwd=self.repo_root,
                capture_output=True,
                text=True,
            )
            out = proc.stdout + proc.stderr
            new_status = "tested" if proc.returncode == 0 else "failed"
            return {**state, "status": new_status, "last_result": out}

        if status == "tested":
            try:
                subprocess.run(["git", "add", "."], cwd=self.repo_root, check=True)
                subprocess.run(
                    ["git", "commit", "-m", f"Self-mod: {state['goal']}"],
                    cwd=self.repo_root,
                    check=True,
                )
            except subprocess.CalledProcessError as exc:
                return {**state, "status": "failed", "last_result": str(exc)}
            return {**state, "status": "merged", "last_result": "patch committed"}

        return {**state, "status": "failed"}


def build_self_mod_graph() -> _SelfModGraph:
    """Return the self-modification graph."""

    return _SelfModGraph()


__all__ = ["SelfModState", "build_self_mod_graph"]

