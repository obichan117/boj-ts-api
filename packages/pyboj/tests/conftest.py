"""Shared test fixtures for pyboj."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from boj_ts_api import DataResponse, SeriesResult

FIXTURES_DIR = Path(__file__).parent / "fixtures"


def _load_fixture(name: str) -> DataResponse:
    """Load a JSON fixture and return a parsed DataResponse."""
    raw = json.loads((FIXTURES_DIR / name).read_text())
    return DataResponse.model_validate(raw)


def _series_results(name: str) -> list[SeriesResult]:
    """Load a fixture and return its RESULTSET as a list of SeriesResult."""
    return _load_fixture(name).RESULTSET


@pytest.fixture()
def csv_text() -> str:
    return (FIXTURES_DIR / "data_code_csv.csv").read_text()


@pytest.fixture()
def exchange_rate_results() -> list[SeriesResult]:
    return _series_results("exchange_rate.json")


@pytest.fixture()
def interest_rate_results() -> list[SeriesResult]:
    return _series_results("interest_rate.json")


@pytest.fixture()
def price_index_results() -> list[SeriesResult]:
    return _series_results("price_index.json")
