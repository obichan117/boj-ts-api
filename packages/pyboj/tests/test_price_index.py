"""Tests for pyboj._domains.price_index."""

from __future__ import annotations

import datetime

import pytest
from boj_ts_api import SeriesResult
from pyboj._domains.price_index import IndexType, PriceIndex


class TestPriceIndex:
    def test_series_code(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.series_code == "PRCG100000"

    def test_dates(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.dates == [
            datetime.date(2024, 1, 1),
            datetime.date(2024, 2, 1),
            datetime.date(2024, 3, 1),
            datetime.date(2024, 4, 1),
        ]

    def test_values(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.values == [120.1, 120.4, 120.8, 121.2]

    def test_values_with_null(self, price_index_results):
        idx = PriceIndex(price_index_results[2])
        assert idx.values == [109.5, 109.8, None, 110.3]


class TestIndexType:
    def test_producer(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.index_type == IndexType.PRODUCER

    def test_services(self, price_index_results):
        idx = PriceIndex(price_index_results[2])
        assert idx.index_type == IndexType.SERVICES

    def test_unknown_type(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST01",
            "NAME_OF_TIME_SERIES": "Some obscure index",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        idx = PriceIndex(result)
        assert idx.index_type == IndexType.OTHER


class TestBaseYear:
    def test_cy2020(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.base_year == "CY2020"

    def test_no_base_year(self, price_index_results):
        idx = PriceIndex(price_index_results[1])
        assert idx.base_year is None


class TestIsYoyChange:
    def test_index_level_is_not_yoy(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        assert idx.is_yoy_change is False

    def test_percent_change_is_yoy(self, price_index_results):
        idx = PriceIndex(price_index_results[1])
        assert idx.is_yoy_change is True


class TestRepr:
    def test_repr_format(self, price_index_results):
        idx = PriceIndex(price_index_results[0])
        r = repr(idx)
        assert "PriceIndex" in r
        assert "PRCG100000" in r
        assert "observations=4" in r


class TestToDataframe:
    def test_dataframe_with_null(self, price_index_results):
        pd = pytest.importorskip("pandas")
        idx = PriceIndex(price_index_results[2])
        df = idx.to_dataframe()
        assert len(df) == 4
        assert pd.isna(df["value"].iloc[2])
