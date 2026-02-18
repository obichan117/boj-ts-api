"""Model for metadata records returned by the Metadata endpoint."""

from __future__ import annotations

from boj_ts_api._types.models.base import BOJBaseModel


class MetadataRecord(BOJBaseModel):
    """A single metadata record from the RESULTSET of the Metadata endpoint."""

    SERIES_CODE: str | None = None
    NAME_OF_TIME_SERIES_J: str | None = None
    NAME_OF_TIME_SERIES: str | None = None
    UNIT_J: str | None = None
    UNIT: str | None = None
    FREQUENCY: str | None = None
    CATEGORY_J: str | None = None
    CATEGORY: str | None = None
    LAYER1: int | str | None = None
    LAYER2: int | str | None = None
    LAYER3: int | str | None = None
    LAYER4: int | str | None = None
    LAYER5: int | str | None = None
    START_OF_THE_TIME_SERIES: str | None = None
    END_OF_THE_TIME_SERIES: str | None = None
    LAST_UPDATE: int | str | None = None
    UNIT_NOTES_J: str | None = None
    UNIT_NOTES: str | None = None
    NOTES_J: str | None = None
    NOTES: str | None = None
