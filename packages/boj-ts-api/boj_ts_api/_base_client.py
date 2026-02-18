"""Shared logic for sync and async BOJ API clients."""

from __future__ import annotations

from typing import Any

from boj_ts_api._types.config import (
    ENDPOINT_DATA_CODE,
    ENDPOINT_DATA_LAYER,
    ENDPOINT_METADATA,
    Format,
    Frequency,
    Lang,
)
from boj_ts_api._utils import _set_optional, _validate_required


class _BaseClient:
    """Shared parameter-building logic for Client and AsyncClient."""

    def __init__(self, lang: Lang = Lang.EN, timeout: float = 30.0) -> None:
        self._lang = lang
        self._timeout = timeout

    def _base_params(self, format_: Format) -> dict[str, str]:
        return {"format": format_.value, "lang": self._lang.value}

    def _data_code_params(
        self,
        db: str,
        code: str,
        *,
        start_date: str | None,
        end_date: str | None,
        start_position: int | None,
        format_: Format,
    ) -> tuple[str, dict[str, Any]]:
        _validate_required(db=db, code=code)
        params = self._base_params(format_=format_)
        params.update({"db": db, "code": code})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        return ENDPOINT_DATA_CODE, params

    def _data_layer_params(
        self,
        db: str,
        frequency: Frequency,
        layer: str,
        *,
        start_date: str | None,
        end_date: str | None,
        start_position: int | None,
        format_: Format,
    ) -> tuple[str, dict[str, Any]]:
        _validate_required(db=db, layer=layer)
        params = self._base_params(format_=format_)
        params.update({"db": db, "frequency": frequency.value, "layer": layer})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        return ENDPOINT_DATA_LAYER, params

    def _metadata_params(
        self,
        db: str,
        *,
        format_: Format,
    ) -> tuple[str, dict[str, Any]]:
        _validate_required(db=db)
        params = self._base_params(format_=format_)
        params["db"] = db
        return ENDPOINT_METADATA, params
