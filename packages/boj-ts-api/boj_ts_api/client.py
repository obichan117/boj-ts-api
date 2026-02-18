"""Synchronous BOJ API client."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from boj_ts_api._parse import parse_data_response, parse_metadata_response
from boj_ts_api._transport import SyncTransport
from boj_ts_api._types.config import (
    ENDPOINT_DATA_CODE,
    ENDPOINT_DATA_LAYER,
    ENDPOINT_METADATA,
    Format,
)
from boj_ts_api._types.models.response import DataResponse, MetadataResponse
from boj_ts_api._types.models.series import SeriesResult
from boj_ts_api._utils import _set_optional, _validate_required


class Client:
    """Synchronous client for the Bank of Japan Time-Series API.

    Usage::

        with Client(lang="en") as client:
            resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    """

    def __init__(
        self,
        lang: str = "en",
        timeout: float = 30.0,
        base_url: str | None = None,
    ) -> None:
        self._lang = lang
        kwargs: dict[str, Any] = {"timeout": timeout}
        if base_url is not None:
            kwargs["base_url"] = base_url
        self._transport = SyncTransport(**kwargs)

    # -- Context manager --

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        self._transport.close()

    # -- Data by Code --

    def get_data_code(
        self,
        db: str,
        code: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> DataResponse:
        """Fetch time-series data by series code(s). Returns a single page."""
        _validate_required(db=db, code=code)
        params = self._base_params(format_=Format.JSON)
        params.update({"db": db, "code": code})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        resp = self._transport.get(ENDPOINT_DATA_CODE, params)
        return parse_data_response(resp)

    def iter_data_code(
        self,
        db: str,
        code: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Iterator[SeriesResult]:
        """Iterate over all series results, auto-paginating via NEXTPOSITION."""
        _validate_required(db=db, code=code)
        start_position: int | None = None
        while True:
            resp = self.get_data_code(
                db=db,
                code=code,
                start_date=start_date,
                end_date=end_date,
                start_position=start_position,
            )
            yield from resp.RESULTSET
            if resp.NEXTPOSITION is None:
                break
            start_position = resp.NEXTPOSITION

    def get_data_code_csv(
        self,
        db: str,
        code: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> str:
        """Fetch time-series data as raw CSV text."""
        _validate_required(db=db, code=code)
        params = self._base_params(format_=Format.CSV)
        params.update({"db": db, "code": code})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        resp = self._transport.get(ENDPOINT_DATA_CODE, params)
        return resp.text

    # -- Data by Layer --

    def get_data_layer(
        self,
        db: str,
        frequency: str,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> DataResponse:
        """Fetch time-series data by hierarchy layer. Returns a single page."""
        _validate_required(db=db, frequency=frequency, layer=layer)
        params = self._base_params(format_=Format.JSON)
        params.update({"db": db, "frequency": frequency, "layer": layer})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        resp = self._transport.get(ENDPOINT_DATA_LAYER, params)
        return parse_data_response(resp)

    def iter_data_layer(
        self,
        db: str,
        frequency: str,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Iterator[SeriesResult]:
        """Iterate over all series results from Layer API, auto-paginating."""
        _validate_required(db=db, frequency=frequency, layer=layer)
        start_position: int | None = None
        while True:
            resp = self.get_data_layer(
                db=db,
                frequency=frequency,
                layer=layer,
                start_date=start_date,
                end_date=end_date,
                start_position=start_position,
            )
            yield from resp.RESULTSET
            if resp.NEXTPOSITION is None:
                break
            start_position = resp.NEXTPOSITION

    def get_data_layer_csv(
        self,
        db: str,
        frequency: str,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> str:
        """Fetch layer data as raw CSV text."""
        _validate_required(db=db, frequency=frequency, layer=layer)
        params = self._base_params(format_=Format.CSV)
        params.update({"db": db, "frequency": frequency, "layer": layer})
        _set_optional(params, startDate=start_date, endDate=end_date, startPosition=start_position)
        resp = self._transport.get(ENDPOINT_DATA_LAYER, params)
        return resp.text

    # -- Metadata --

    def get_metadata(
        self,
        db: str,
    ) -> MetadataResponse:
        """Fetch metadata for a database."""
        _validate_required(db=db)
        params = self._base_params(format_=Format.JSON)
        params["db"] = db
        resp = self._transport.get(ENDPOINT_METADATA, params)
        return parse_metadata_response(resp)

    def get_metadata_csv(
        self,
        db: str,
    ) -> str:
        """Fetch metadata as raw CSV text."""
        _validate_required(db=db)
        params = self._base_params(format_=Format.CSV)
        params["db"] = db
        resp = self._transport.get(ENDPOINT_METADATA, params)
        return resp.text

    # -- Helpers --

    def _base_params(self, format_: Format) -> dict[str, str]:
        return {"format": format_.value, "lang": self._lang}
