"""Shared test fixtures for pyboj."""

from __future__ import annotations

from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def csv_text() -> str:
    return (FIXTURES_DIR / "data_code_csv.csv").read_text()
