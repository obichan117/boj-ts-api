"""Tests for the asynchronous AsyncClient."""

from __future__ import annotations

import httpx
import pytest
import respx
from boj_ts_api import AsyncClient, Frequency, Lang
from boj_ts_api._types.config import (
    BASE_URL,
    ENDPOINT_DATA_CODE,
    ENDPOINT_DATA_LAYER,
    ENDPOINT_METADATA,
)


class TestAsyncGetDataCode:
    @respx.mock
    @pytest.mark.asyncio
    async def test_basic_request(self, data_code_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=data_code_json)
        )
        async with AsyncClient(lang=Lang.EN) as client:
            resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")

        assert resp.STATUS == 200
        assert len(resp.RESULTSET) == 1

    @respx.mock
    @pytest.mark.asyncio
    async def test_csv_returns_text(self, csv_text: str):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, text=csv_text)
        )
        async with AsyncClient(lang=Lang.EN) as client:
            result = await client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")

        assert "SERIES_CODE" in result


class TestAsyncIterDataCode:
    @respx.mock
    @pytest.mark.asyncio
    async def test_two_pages(self, data_code_page1_json: dict, data_code_page2_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            side_effect=[
                httpx.Response(200, json=data_code_page1_json),
                httpx.Response(200, json=data_code_page2_json),
            ]
        )
        results = []
        async with AsyncClient(lang=Lang.EN) as client:
            async for item in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
                results.append(item)

        assert len(results) == 2
        assert results[0].VALUES.SURVEY_DATES == [202401, 202402]
        assert results[1].VALUES.SURVEY_DATES == [202403, 202404]


class TestAsyncGetDataLayer:
    @respx.mock
    @pytest.mark.asyncio
    async def test_basic_request(self, data_layer_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_LAYER}").mock(
            return_value=httpx.Response(200, json=data_layer_json)
        )
        async with AsyncClient(lang=Lang.EN) as client:
            resp = await client.get_data_layer(db="FM08", frequency=Frequency.D, layer="1,1")

        assert resp.STATUS == 200
        assert resp.RESULTSET[0].SERIES_CODE == "MAINAVG"


class TestAsyncGetMetadata:
    @respx.mock
    @pytest.mark.asyncio
    async def test_basic_request(self, metadata_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_METADATA}").mock(
            return_value=httpx.Response(200, json=metadata_json)
        )
        async with AsyncClient(lang=Lang.EN) as client:
            resp = await client.get_metadata(db="FM08")

        assert resp.STATUS == 200
        assert len(resp.RESULTSET) == 2
