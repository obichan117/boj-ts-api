"""Tests for pagination via iter_data_code and iter_data_layer."""

from __future__ import annotations

import httpx
import respx

from boj_ts_api.client.sync_client import BOJClient
from boj_ts_api.config import BASE_URL, ENDPOINT_DATA_CODE, ENDPOINT_DATA_LAYER


class TestIterDataCode:
    @respx.mock
    def test_single_page(self, data_code_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=data_code_json)
        )
        with BOJClient(lang="en") as client:
            results = list(client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"))

        assert len(results) == 1
        assert results[0].SERIES_CODE == "TK99F1000601GCQ01000"

    @respx.mock
    def test_two_pages(self, data_code_page1_json: dict, data_code_page2_json: dict):
        route = respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            side_effect=[
                httpx.Response(200, json=data_code_page1_json),
                httpx.Response(200, json=data_code_page2_json),
            ]
        )
        with BOJClient(lang="en") as client:
            results = list(client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"))

        assert route.call_count == 2
        assert len(results) == 2
        # Page 1 data
        assert results[0].VALUES.SURVEY_DATES == [202401, 202402]
        # Page 2 data
        assert results[1].VALUES.SURVEY_DATES == [202403, 202404]


class TestIterDataLayer:
    @respx.mock
    def test_single_page(self, data_layer_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_LAYER}").mock(
            return_value=httpx.Response(200, json=data_layer_json)
        )
        with BOJClient(lang="en") as client:
            results = list(client.iter_data_layer(db="FM08", frequency="D", layer="1,1"))

        assert len(results) == 1
        assert results[0].SERIES_CODE == "FM08'MAINAVG"
