"""Tests for CSV helper."""

from __future__ import annotations

from pyboj import csv_to_dataframe


class TestCsvToDataframe:
    def test_basic_conversion(self, csv_text: str):
        df = csv_to_dataframe(csv_text)
        assert len(df) == 4
        assert "SERIES_CODE" in df.columns
        assert "VALUE" in df.columns
        assert df["VALUE"].iloc[0] == 106.9

    def test_column_names(self, csv_text: str):
        df = csv_to_dataframe(csv_text)
        expected = {
            "SERIES_CODE",
            "NAME_OF_TIME_SERIES",
            "UNIT",
            "FREQUENCY",
            "CATEGORY",
            "LAST_UPDATE",
            "SURVEY_DATE",
            "VALUE",
        }
        assert set(df.columns) == expected
