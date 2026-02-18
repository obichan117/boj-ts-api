"""Synchronous BOJ API client."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from boj_ts_api._base_client import _BaseClient
from boj_ts_api._parse import parse_data_response, parse_metadata_response
from boj_ts_api._transport import SyncTransport
from boj_ts_api._types.config import DEFAULT_TIMEOUT, Format, Frequency, Lang
from boj_ts_api._types.models.response import DataResponse, MetadataResponse
from boj_ts_api._types.models.series import SeriesResult


class Client(_BaseClient):
    """Synchronous client for the Bank of Japan Time-Series API.

    Usage::

        with Client(lang=Lang.EN) as client:
            resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    """

    def __init__(
        self,
        lang: Lang = Lang.EN,
        timeout: float = DEFAULT_TIMEOUT,
        base_url: str | None = None,
    ) -> None:
        super().__init__(lang=lang, timeout=timeout)
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
        path, params = self._data_code_params(
            db, code, start_date=start_date, end_date=end_date,
            start_position=start_position, format_=Format.JSON,
        )
        return parse_data_response(self._transport.get(path, params))

    def iter_data_code(
        self,
        db: str,
        code: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Iterator[SeriesResult]:
        """Iterate over all series results, auto-paginating via NEXTPOSITION."""
        start_position: int | None = None
        while True:
            resp = self.get_data_code(
                db=db, code=code, start_date=start_date,
                end_date=end_date, start_position=start_position,
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
        path, params = self._data_code_params(
            db, code, start_date=start_date, end_date=end_date,
            start_position=start_position, format_=Format.CSV,
        )
        return self._transport.get(path, params).text

    # -- Data by Layer --

    def get_data_layer(
        self,
        db: str,
        frequency: Frequency,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> DataResponse:
        """Fetch time-series data by hierarchy layer. Returns a single page."""
        path, params = self._data_layer_params(
            db, frequency, layer, start_date=start_date, end_date=end_date,
            start_position=start_position, format_=Format.JSON,
        )
        return parse_data_response(self._transport.get(path, params))

    def iter_data_layer(
        self,
        db: str,
        frequency: Frequency,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> Iterator[SeriesResult]:
        """Iterate over all series results from Layer API, auto-paginating."""
        start_position: int | None = None
        while True:
            resp = self.get_data_layer(
                db=db, frequency=frequency, layer=layer,
                start_date=start_date, end_date=end_date,
                start_position=start_position,
            )
            yield from resp.RESULTSET
            if resp.NEXTPOSITION is None:
                break
            start_position = resp.NEXTPOSITION

    def get_data_layer_csv(
        self,
        db: str,
        frequency: Frequency,
        layer: str,
        *,
        start_date: str | None = None,
        end_date: str | None = None,
        start_position: int | None = None,
    ) -> str:
        """Fetch layer data as raw CSV text."""
        path, params = self._data_layer_params(
            db, frequency, layer, start_date=start_date, end_date=end_date,
            start_position=start_position, format_=Format.CSV,
        )
        return self._transport.get(path, params).text

    # -- Metadata --

    def get_metadata(self, db: str) -> MetadataResponse:
        """Fetch metadata for a database."""
        path, params = self._metadata_params(db, format_=Format.JSON)
        return parse_metadata_response(self._transport.get(path, params))

    def get_metadata_csv(self, db: str) -> str:
        """Fetch metadata as raw CSV text."""
        path, params = self._metadata_params(db, format_=Format.CSV)
        return self._transport.get(path, params).text
