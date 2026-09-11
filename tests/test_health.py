"""S0 integration: GET /health on the running stack reports db ok and the loaded network."""

from __future__ import annotations

import os

import httpx
import pytest

pytestmark = pytest.mark.integration

API_URL = os.environ.get("API_URL", "http://localhost:8000")


def test_health_reports_db_and_network():
    r = httpx.get(f"{API_URL}/health", timeout=10)
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["db"] == "ok"
    assert body["network"]["name"] == os.environ.get("NETWORK_NAME", "Net3")
    assert body["network"]["node_count"] > 0
    assert body["network"]["link_count"] > 0
    assert body["versions"]["jax"] and body["versions"]["wntr"]
