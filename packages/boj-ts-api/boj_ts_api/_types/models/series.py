"""Models for time-series data returned by Code and Layer endpoints."""

from __future__ import annotations

from pydantic import Field

from boj_ts_api._types.models.base import BOJBaseModel


class SeriesValues(BOJBaseModel):
    """Nested time-series values within a series result."""

    SURVEY_DATES: list[int | str] = Field(default_factory=list)
    VALUES: list[float | str | None] = Field(default_factory=list)


class SeriesResult(BOJBaseModel):
    """A single series item from the RESULTSET of Code/Layer endpoints."""

    SERIES_CODE: str
    NAME_OF_TIME_SERIES_J: str | None = None
    NAME_OF_TIME_SERIES: str | None = None
    UNIT_J: str | None = None
    UNIT: str | None = None
    FREQUENCY: str | None = None
    CATEGORY_J: str | None = None
    CATEGORY: str | None = None
    LAST_UPDATE: int | str | None = None
    VALUES: SeriesValues = Field(default_factory=SeriesValues)
