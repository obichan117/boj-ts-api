"""Configuration constants and enumerations for the BOJ Time-Series API."""

from __future__ import annotations

from enum import Enum

BASE_URL = "https://www.stat-search.boj.or.jp"

# Endpoint paths (case-sensitive)
ENDPOINT_DATA_CODE = "/api/v1/getDataCode"
ENDPOINT_DATA_LAYER = "/api/v1/getDataLayer"
ENDPOINT_METADATA = "/api/v1/getMetadata"

# Defaults
DEFAULT_TIMEOUT = 30.0

# API limits
MAX_SERIES_PER_REQUEST = 250
MAX_DATA_POINTS_PER_REQUEST = 60_000
MAX_LAYER_SERIES = 1_250


class Lang(str, Enum):
    """Language for API responses."""

    JP = "jp"
    EN = "en"


class Format(str, Enum):
    """Response format."""

    JSON = "json"
    CSV = "csv"


class Frequency(str, Enum):
    """Time-series frequency."""

    CY = "CY"  # Calendar Year
    FY = "FY"  # Fiscal Year
    CH = "CH"  # Calendar Half
    FH = "FH"  # Fiscal Half
    Q = "Q"  # Quarterly
    M = "M"  # Monthly
    W = "W"  # Weekly
    D = "D"  # Daily
