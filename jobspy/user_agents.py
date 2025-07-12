"""Utilities for building a rotating list of modern user agents."""

from __future__ import annotations

import json
import requests
from typing import List, Optional


STATIC_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]

_CACHED_USER_AGENTS: Optional[List[str]] = None

def _fetch_dynamic_user_agents(limit: int = 20) -> List[str]:
    """Return a list of recent user agent strings from fake-useragent data."""

    url = (
        "https://raw.githubusercontent.com/"
        "fake-useragent/fake-useragent/master/"
        "src/fake_useragent/data/browsers.jsonl"
    )
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        lines = resp.text.splitlines()[:limit]
        return [json.loads(line)["useragent"] for line in lines]
    except Exception:
        # Gracefully fall back to the static list on any failure
        return []


def get_default_user_agents() -> List[str]:
    """
    Returns a list of default user agents, fetching dynamic ones on the first call.
    Caches the result for subsequent calls to avoid repeated network requests.
    """
    global _CACHED_USER_AGENTS
    if _CACHED_USER_AGENTS is not None:
        return _CACHED_USER_AGENTS

    dynamic_agents = _fetch_dynamic_user_agents()
    _CACHED_USER_AGENTS = dynamic_agents + STATIC_USER_AGENTS
    return _CACHED_USER_AGENTS


def get_mobile_user_agents() -> List[str]:
    """
    Returns a list of mobile user agents, prioritizing iPhone user agents to avoid blocking.
    """
    all_agents = get_default_user_agents()
    iphone_agents = [agent for agent in all_agents if "iPhone" in agent]

    if iphone_agents:
        return iphone_agents

    # Fallback to a generic mobile user agent if no iPhone UAs are found
    mobile_agents = [agent for agent in all_agents if "Mobile" in agent]
    if mobile_agents:
        return mobile_agents

    # As a last resort, return a known good static mobile user agent
    return [
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ]
