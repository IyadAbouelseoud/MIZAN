"""MIZAN API (Stage 0): FastAPI app exposing GET /health.

Stage 5 adds POST /runs, GET /runs/{id}, cancel, and the loss-curve stream.
"""

from __future__ import annotations

import os
from importlib.metadata import PackageNotFoundError, version

import psycopg
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="MIZAN API", version="0.0.1")


def _pkg_version(name: str) -> str | None:
    try:
        return version(name)
    except PackageNotFoundError:
        return None


def _db_and_network() -> tuple[str, dict | None]:
    """Return ("ok", network-or-None) or ("error: ...", None)."""
    dsn = os.environ.get("DATABASE_URL")
    if not dsn:
        return "error: DATABASE_URL is not set", None
    try:
        with psycopg.connect(dsn, connect_timeout=3) as conn, conn.cursor() as cur:
            cur.execute(
                "SELECT name, node_count, link_count, pump_count, tank_count "
                "FROM networks ORDER BY loaded_at DESC LIMIT 1"
            )
            row = cur.fetchone()
    except psycopg.Error as exc:
        return f"error: {exc.__class__.__name__}: {exc}".strip(), None
    if row is None:
        return "ok", None
    name, nodes, links, pumps, tanks = row
    return "ok", {
        "name": name,
        "node_count": nodes,
        "link_count": links,
        "pump_count": pumps,
        "tank_count": tanks,
    }


@app.get("/health")
def health() -> JSONResponse:
    db_status, network = _db_and_network()
    body = {
        "status": "ok" if db_status == "ok" else "degraded",
        "db": db_status,
        "network": network,
        "versions": {"jax": _pkg_version("jax"), "wntr": _pkg_version("wntr")},
    }
    return JSONResponse(body, status_code=200 if db_status == "ok" else 503)
