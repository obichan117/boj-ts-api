"""Envelope models for API responses."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from boj_ts_api.models.base import BOJBaseModel
from boj_ts_api.models.metadata import MetadataRecord
from boj_ts_api.models.series import SeriesResult


class DataResponse(BOJBaseModel):
    """Envelope for Code/Layer API JSON responses."""

    STATUS: int
    MESSAGEID: str = ""
    MESSAGE: str = ""
    DATE: str = ""
    PARAMETER: dict[str, Any] | None = None
    NEXTPOSITION: int | None = None
    RESULTSET: list[SeriesResult] = Field(default_factory=list)


class MetadataResponse(BOJBaseModel):
    """Envelope for Metadata API JSON responses."""

    STATUS: int
    MESSAGEID: str = ""
    MESSAGE: str = ""
    DATE: str = ""
    PARAMETER: dict[str, Any] | None = None
    NEXTPOSITION: int | None = None
    RESULTSET: list[MetadataRecord] = Field(default_factory=list)
