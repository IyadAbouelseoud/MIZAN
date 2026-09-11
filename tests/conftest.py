"""Shared test configuration (Stage 0)."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def net3_path() -> Path:
    return ROOT / "data" / "networks" / "Net3.inp"
