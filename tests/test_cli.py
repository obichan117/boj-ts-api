"""Tests for the CLI."""

from __future__ import annotations

import json

import httpx
import respx
from click.testing import CliRunner

from boj_ts_api.cli import main
from boj_ts_api.config import BASE_URL, ENDPOINT_DATA_CODE, ENDPOINT_METADATA


class TestCLIGetDataCode:
    @respx.mock
    def test_json_output(self, data_code_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=data_code_json)
        )
        runner = CliRunner()
        result = runner.invoke(main, ["get-data-code", "--db", "CO", "--code", "TK99F1000601GCQ01000"])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert output["STATUS"] == 200

    @respx.mock
    def test_csv_output(self, csv_text: str):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, text=csv_text)
        )
        runner = CliRunner()
        result = runner.invoke(
            main,
            ["get-data-code", "--db", "CO", "--code", "TK99F1000601GCQ01000", "--format", "csv"],
        )
        assert result.exit_code == 0
        assert "SERIES_CODE" in result.output


class TestCLIGetMetadata:
    @respx.mock
    def test_json_output(self, metadata_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_METADATA}").mock(
            return_value=httpx.Response(200, json=metadata_json)
        )
        runner = CliRunner()
        result = runner.invoke(main, ["get-metadata", "--db", "FM08"])
        assert result.exit_code == 0
        output = json.loads(result.output)
        assert len(output["RESULTSET"]) == 2


class TestCLIErrorHandling:
    @respx.mock
    def test_api_error(self, error_json: dict):
        respx.get(f"{BASE_URL}{ENDPOINT_DATA_CODE}").mock(
            return_value=httpx.Response(200, json=error_json)
        )
        runner = CliRunner()
        result = runner.invoke(main, ["get-data-code", "--db", "CO", "--code", "INVALID"])
        assert result.exit_code != 0
        assert "Error" in result.output or "missing" in result.output.lower()

    def test_missing_required(self):
        runner = CliRunner()
        result = runner.invoke(main, ["get-data-code", "--db", "CO"])
        assert result.exit_code != 0
