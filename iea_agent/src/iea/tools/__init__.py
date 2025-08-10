"""
Tool registry. Tools are individually importable and also exposed as a list
for quick binding to LLMs that support tool-calling via LangChain.
"""
from .web_search import tavily_search
from .browser import visit_url
from .fs_git import read_file, write_patch, run_tests, merge_and_reload
from .shell import safe_shell
from .parser import extract_text

# Optional HTTP client tools (requires httpx)
try:  # pragma: no cover - dependency optional
    from .http_client import http_get, http_post
    _HTTP_FUNCS = [http_get, http_post]
except Exception:  # httpx not installed
    _HTTP_FUNCS = []

TOOLS = [
    tavily_search,
    visit_url,
    read_file,
    write_patch,
    run_tests,
    merge_and_reload,
    safe_shell,
] + _HTTP_FUNCS + [
    extract_text,
]

__all__ = [t.name for t in TOOLS]  # type: ignore[attr-defined]
