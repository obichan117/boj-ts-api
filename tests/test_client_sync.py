"""Tests for the synchronous BOJClient."""

from __future__ import annotations

import httpx
import respx

from boj_ts_api.client.sync_client import BOJClient
from boj_ts_api.config import BASE_URL, ENDPOINT_DATA_CODE, ENDPOINT_DATA_LAYER, ENDPOINT_METADATA


class TestGetDataCode:
    @respx.mock
    def test_basic_request(self, data_code_json: dict):
        route = respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=data_code_json)
        )
        with BOJClient(lang="en") as client:
            resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")

        assert route.called
        assert resp.STATUS == 200
        assert len(resp.RESULTSET) == 1
        assert resp.RESULTSET[0].SERIES_CODE == "TK99F1000601GCQ01000"

    @respx.mock
    def test_with_date_range(self, data_code_json: dict):
        route = respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=data_code_json)
        )
        with BOJClient(lang="en") as client:
            resp = client.get_data_code(
                db="CO",
                code="TK99F1000601GCQ01000",
                start_date="202401",
                end_date="202404",
            )

        assert route.called
        request = route.calls[0].request
        assert "startDate=202401" in str(request.url)
        assert "endDate=202404" in str(request.url)
        assert resp.STATUS == 200

    @respx.mock
    def test_csv_returns_text(self, csv_text: str):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, text=csv_text)
        )
        with BOJClient(lang="en") as client:
            result = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")

        assert "SERIES_CODE" in result
        assert "TK99F1000601GCQ01000" in result


class TestGetDataLayer:
    @respx.mock
    def test_basic_request(self, data_layer_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_LAYER}").mock(
            return_value=httpx.Response(200, json=data_layer_json)
        )
        with BOJClient(lang="en") as client:
            resp = client.get_data_layer(db="FM08", frequency="D", layer="1,1")

        assert resp.STATUS == 200
        assert resp.RESULTSET[0].SERIES_CODE == "FM08'MAINAVG"


class TestGetMetadata:
    @respx.mock
    def test_basic_request(self, metadata_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_METADATA}").mock(
            return_value=httpx.Response(200, json=metadata_json)
        )
        with BOJClient(lang="en") as client:
            resp = client.get_metadata(db="FM08")

        assert resp.STATUS == 200
        assert len(resp.RESULTSET) == 2

    @respx.mock
    def test_csv_returns_text(self):
        csv = "SERIES_CODE,FREQUENCY\nFM08'MAINAVG,D\n"
        respx.get(f"{BASE_URL}{ENDPOINT_METADATA}").mock(
            return_value=httpx.Response(200, text=csv)
        )
        with BOJClient(lang="en") as client:
            result = client.get_metadata_csv(db="FM08")

        assert "FM08'MAINAVG" in result
