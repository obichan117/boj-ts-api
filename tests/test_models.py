"""Tests for Pydantic models."""

from __future__ import annotations

from boj_ts_api.models import (
    DataResponse,
    MetadataRecord,
    MetadataResponse,
    SeriesResult,
    SeriesValues,
)


class TestSeriesValues:
    def test_parse_numeric_values(self):
        sv = SeriesValues(
            SURVEY_DATES=[202401, 202402],
            VALUES=[106.9, 106.8],
        )
        assert sv.SURVEY_DATES == [202401, 202402]
        assert sv.VALUES == [106.9, 106.8]

    def test_parse_with_nulls(self):
        sv = SeriesValues(
            SURVEY_DATES=[202401, 202402, 202403],
            VALUES=[106.9, None, 107.2],
        )
        assert sv.VALUES[1] is None

    def test_defaults_to_empty(self):
        sv = SeriesValues()
        assert sv.SURVEY_DATES == []
        assert sv.VALUES == []


class TestSeriesResult:
    def test_parse_full(self, data_code_json: dict):
        item = data_code_json["RESULTSET"][0]
        sr = SeriesResult.model_validate(item)
        assert sr.SERIES_CODE == "TK99F1000601GCQ01000"
        assert sr.FREQUENCY == "M"
        assert sr.UNIT == "CY2020=100"
        assert len(sr.VALUES.SURVEY_DATES) == 4
        assert sr.VALUES.VALUES[0] == 106.9

    def test_minimal(self):
        sr = SeriesResult(SERIES_CODE="TEST001")
        assert sr.SERIES_CODE == "TEST001"
        assert sr.VALUES.SURVEY_DATES == []


class TestDataResponse:
    def test_parse_success(self, data_code_json: dict):
        resp = DataResponse.model_validate(data_code_json)
        assert resp.STATUS == 200
        assert resp.NEXTPOSITION is None
        assert len(resp.RESULTSET) == 1
        assert resp.RESULTSET[0].SERIES_CODE == "TK99F1000601GCQ01000"

    def test_parse_paginated(self, data_code_page1_json: dict):
        resp = DataResponse.model_validate(data_code_page1_json)
        assert resp.NEXTPOSITION == 251

    def test_parse_error(self, error_json: dict):
        resp = DataResponse.model_validate(error_json)
        assert resp.STATUS == 400
        assert resp.MESSAGEID == "E0001"
        assert "missing" in resp.MESSAGE.lower()


class TestMetadataRecord:
    def test_parse_full(self, metadata_json: dict):
        item = metadata_json["RESULTSET"][0]
        rec = MetadataRecord.model_validate(item)
        assert rec.SERIES_CODE == "FM08'MAINAVG"
        assert rec.FREQUENCY == "D"
        assert rec.LAYER1 == "1"
        assert rec.LAYER3 is None
        assert rec.NOTES == "Source: BOJ"

    def test_minimal(self):
        rec = MetadataRecord()
        assert rec.SERIES_CODE is None
        assert rec.LAYER1 is None


class TestMetadataResponse:
    def test_parse_success(self, metadata_json: dict):
        resp = MetadataResponse.model_validate(metadata_json)
        assert resp.STATUS == 200
        assert len(resp.RESULTSET) == 2
        assert resp.RESULTSET[0].SERIES_CODE == "FM08'MAINAVG"
        assert resp.RESULTSET[1].SERIES_CODE == "FM08'MAINHIGH"
