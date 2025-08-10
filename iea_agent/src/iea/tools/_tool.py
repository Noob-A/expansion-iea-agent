from __future__ import annotations

"""Minimal fallback for LangChain's tool decorator."""
from typing import Any, Callable

try:  # pragma: no cover - only exercised when langchain is installed
    from langchain_core.tools import tool as lc_tool  # type: ignore
except Exception:  # langchain_core not installed
    lc_tool = None

class SimpleTool:
    """Simple callable object mimicking LangChain's tool interface."""
    def __init__(self, func: Callable[..., Any], name: str):
        self.func = func
        self.name = name or func.__name__
        self.description = func.__doc__ or ""

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        return self.func(*args, **kwargs)

    def invoke(self, inputs: Any) -> Any:
        if isinstance(inputs, dict):
            return self.func(**inputs)
        return self.func(inputs)

def tool(name: str, return_direct: bool = False):  # pragma: no cover - thin wrapper
    if lc_tool:
        return lc_tool(name, return_direct=return_direct)
    def decorator(fn: Callable[..., Any]) -> SimpleTool:
        return SimpleTool(fn, name)
    return decorator

__all__ = ["tool"]
