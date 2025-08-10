from __future__ import annotations

"""Simplified targeting graph used for tests.

The original project uses LangGraph and LLMs to plan and execute tasks.
For the unit tests in this kata we only need a minimal state machine that
mimics the interface and returns deterministic transitions.
"""

from typing import TypedDict, List, Literal


class TargetState(TypedDict):
    target: str
    tasks: List[str]
    current: str | None
    mode: Literal["decide_or_plan", "execute", "done"]
    log: List[str]


class _TargetingGraph:
    def invoke(self, state: TargetState) -> TargetState:
        if state.get("mode") == "decide_or_plan":
            tasks = state.get("tasks") or [f"Research: {state['target']}"]
            return {
                **state,
                "tasks": tasks,
                "current": tasks[0],
                "mode": "execute",
                "log": state.get("log", []) + ["planned"],
            }
        if state.get("mode") == "execute":
            return {**state, "mode": "done", "log": state.get("log", []) + ["executed"]}
        return state


def build_targeting_graph() -> _TargetingGraph:
    return _TargetingGraph()

__all__ = ["build_targeting_graph", "TargetState"]
