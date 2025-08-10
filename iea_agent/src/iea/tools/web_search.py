from __future__ import annotations
from typing import List
try:  # pragma: no cover - optional dependency
    from langchain_tavily import TavilySearchResults  # type: ignore
except Exception:  # langchain_tavily may not be installed
    TavilySearchResults = None

from ._tool import tool
from ..config import SETTINGS

"""
Tavily search tool.
We use the lightweight `TavilySearchResults` wrapper from LangChain that returns
structured results for a given query.
"""

if TavilySearchResults and SETTINGS.tavily_api_key:
    tavily = TavilySearchResults(tavily_api_key=SETTINGS.tavily_api_key, max_results=5)
else:  # pragma: no cover - exercised when dependency missing
    tavily = None

@tool("tavily_search", return_direct=False)
def tavily_search(query: str) -> List[dict]:
    """
    Search the web with Tavily and return top results with URLs & snippets.
    Input: query (str)
    Output: List[dict] with keys: 'title', 'url', 'content' (snippet)
    """
    if not SETTINGS.tavily_api_key or tavily is None:
        return [{"title": "Tavily disabled", "url": "", "content": "No API key or dependency"}]
    try:
        return tavily.invoke({"query": query})  # type: ignore[union-attr]
    except Exception as e:  # pragma: no cover - network errors
        return [{"title": "Search error", "url": "", "content": f"{type(e).__name__}: {e}"}]
