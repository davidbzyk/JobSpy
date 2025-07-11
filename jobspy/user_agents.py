"""Utilities for building a rotating list of modern user agents."""

from __future__ import annotations

import json
import requests


STATIC_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/117.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0",
]


def _fetch_dynamic_user_agents(limit: int = 20) -> list[str]:
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


DEFAULT_USER_AGENTS = _fetch_dynamic_user_agents() + STATIC_USER_AGENTS
