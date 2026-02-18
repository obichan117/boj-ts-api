"""Tests for exception handling."""

from __future__ import annotations

import httpx
import pytest
import respx

from boj_ts_api.client.sync_client import BOJClient
from boj_ts_api.config import BASE_URL, ENDPOINT_DATA_CODE
from boj_ts_api.exceptions import BOJAPIError, BOJRequestError, BOJValidationError


class TestBOJValidationError:
    def test_empty_db(self):
        with BOJClient(lang="en") as client:
            with pytest.raises(BOJValidationError, match="db"):
                client.get_data_code(db="", code="X")

    def test_empty_code(self):
        with BOJClient(lang="en") as client:
            with pytest.raises(BOJValidationError, match="code"):
                client.get_data_code(db="CO", code="")


class TestBOJAPIError:
    @respx.mock
    def test_api_error_status(self, error_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=error_json)
        )
        with BOJClient(lang="en") as client:
            with pytest.raises(BOJAPIError) as exc_info:
                client.get_data_code(db="CO", code="INVALID")

        assert exc_info.value.status == 400
        assert exc_info.value.message_id == "E0001"
        assert "missing" in exc_info.value.api_message.lower()


class TestBOJRequestError:
    @respx.mock
    def test_network_error(self):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            side_effect=httpx.ConnectError("Connection refused")
        )
        with BOJClient(lang="en") as client:
            with pytest.raises(BOJRequestError):
                client.get_data_code(db="CO", code="X")

    @respx.mock
    def test_http_500(self):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(500)
        )
        with BOJClient(lang="en") as client:
            with pytest.raises(BOJRequestError, match="500"):
                client.get_data_code(db="CO", code="X")
