"""Envelope models for API responses."""

from __future__ import annotations

from typing import Any

from pydantic import Field

from boj_ts_api._types.models.base import BOJBaseModel
from boj_ts_api._types.models.metadata import MetadataRecord
from boj_ts_api._types.models.series import SeriesResult


class ResponseEnvelope(BOJBaseModel):
    """Shared envelope fields for all BOJ API JSON responses."""

    STATUS: int
    MESSAGEID: str = ""
    MESSAGE: str = ""
    DATE: str = ""
    PARAMETER: dict[str, Any] | None = None
    NEXTPOSITION: int | None = None


class DataResponse(ResponseEnvelope):
    """Envelope for Code/Layer API JSON responses."""

    RESULTSET: list[SeriesResult] = Field(default_factory=list)


class MetadataResponse(ResponseEnvelope):
    """Envelope for Metadata API JSON responses."""

    RESULTSET: list[MetadataRecord] = Field(default_factory=list)
