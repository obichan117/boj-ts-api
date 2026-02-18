"""Shared test fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture()
def fixtures_dir() -> Path:
    return FIXTURES_DIR


def load_fixture(name: str) -> dict:
    """Load a JSON fixture by filename."""
    return json.loads((FIXTURES_DIR / name).read_text())


@pytest.fixture()
def data_code_json() -> dict:
    return load_fixture("data_code_response.json")


@pytest.fixture()
def data_code_page1_json() -> dict:
    return load_fixture("data_code_paginated_page1.json")


@pytest.fixture()
def data_code_page2_json() -> dict:
    return load_fixture("data_code_paginated_page2.json")


@pytest.fixture()
def data_layer_json() -> dict:
    return load_fixture("data_layer_response.json")


@pytest.fixture()
def metadata_json() -> dict:
    return load_fixture("metadata_response.json")


@pytest.fixture()
def error_json() -> dict:
    return load_fixture("error_response.json")


@pytest.fixture()
def csv_text() -> str:
    return (FIXTURES_DIR / "data_code_csv.csv").read_text()
