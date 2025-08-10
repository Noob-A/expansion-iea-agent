from __future__ import annotations

"""Simplified self-modification graph for tests.

The real project uses an LLM-driven LangGraph that patches files and runs
unit tests.  For the purposes of unit testing we only provide a minimal
state machine that exercises the expected transitions.
"""

from typing import TypedDict, Literal


class SelfModState(TypedDict):
    goal: str
    file_list: list[str]
    last_result: str
    status: Literal["start", "patched", "tested", "merged", "failed"]
    attempts: int


class _SelfModGraph:
    def invoke(self, state: SelfModState) -> SelfModState:
        status = state.get("status")
        if status == "start":
            return {**state, "last_result": "patch generated", "status": "patched"}
        if status == "patched":
            return {**state, "last_result": "tests executed", "status": "tested"}
        if status == "tested":
            return {**state, "status": "merged"}
        return {**state, "status": "failed"}


def build_self_mod_graph() -> _SelfModGraph:
    return _SelfModGraph()

__all__ = ["build_self_mod_graph", "SelfModState"]
