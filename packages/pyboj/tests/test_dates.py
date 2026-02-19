"""Tests for pyboj._parsing.dates."""

from __future__ import annotations

import datetime

import pytest
from pyboj._parsing.dates import parse_survey_date, parse_survey_dates


class TestParseSurveyDate:
    def test_yyyymmdd_int(self):
        assert parse_survey_date(20240104) == datetime.date(2024, 1, 4)

    def test_yyyymmdd_str(self):
        assert parse_survey_date("20240104") == datetime.date(2024, 1, 4)

    def test_yyyymm_int(self):
        assert parse_survey_date(202401) == datetime.date(2024, 1, 1)

    def test_yyyymm_str(self):
        assert parse_survey_date("202412") == datetime.date(2024, 12, 1)

    def test_yyyy_int(self):
        assert parse_survey_date(2024) == datetime.date(2024, 1, 1)

    def test_yyyy_str(self):
        assert parse_survey_date("2024") == datetime.date(2024, 1, 1)

    def test_invalid_length_raises(self):
        with pytest.raises(ValueError, match="Cannot parse survey date"):
            parse_survey_date(12345)

    def test_invalid_too_short_raises(self):
        with pytest.raises(ValueError, match="Cannot parse survey date"):
            parse_survey_date(99)


class TestParseSurveyDates:
    def test_mixed_formats(self):
        result = parse_survey_dates([20240104, 202402, 2024])
        assert result == [
            datetime.date(2024, 1, 4),
            datetime.date(2024, 2, 1),
            datetime.date(2024, 1, 1),
        ]

    def test_empty_list(self):
        assert parse_survey_dates([]) == []

    def test_none_entries_preserved(self):
        result = parse_survey_dates([20240104, None, 202402])
        assert result == [
            datetime.date(2024, 1, 4),
            None,
            datetime.date(2024, 2, 1),
        ]
