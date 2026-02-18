"""Tests for pyboj._domains.exchange_rate."""

from __future__ import annotations

import datetime

import pytest
from boj_ts_api import SeriesResult
from pyboj._domains.exchange_rate import ExchangeRate, RateType


class TestExchangeRate:
    def test_series_code(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.series_code == "FXERD01"

    def test_name(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.name == "U.S.dollar/Yen Spot Rate at 9 A.M."

    def test_name_jp(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.name_jp == "ドル・円 スポット 9時時点"

    def test_dates(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.dates == [datetime.date(2024, 1, 4), datetime.date(2024, 1, 5)]

    def test_values(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.values == [141.75, 144.62]

    def test_frequency(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.frequency == "DAILY"


class TestCurrencyPair:
    def test_usd_jpy(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.currency_pair == "USD/JPY"

    def test_eur_jpy(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[1])
        assert rate.currency_pair == "EUR/JPY"

    def test_unknown_currency(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST01",
            "NAME_OF_TIME_SERIES": "Unknown currency/Yen Rate",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = ExchangeRate(result)
        assert rate.currency_pair is None


class TestRateType:
    def test_spot_9am(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        assert rate.rate_type == RateType.SPOT_9AM

    def test_central(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[1])
        assert rate.rate_type == RateType.CENTRAL

    def test_highest(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[2])
        assert rate.rate_type == RateType.HIGHEST

    def test_unknown_rate_type(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST01",
            "NAME_OF_TIME_SERIES": "Some obscure metric",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = ExchangeRate(result)
        assert rate.rate_type == RateType.OTHER


class TestRepr:
    def test_repr_format(self, exchange_rate_results):
        rate = ExchangeRate(exchange_rate_results[0])
        r = repr(rate)
        assert "ExchangeRate" in r
        assert "FXERD01" in r
        assert "observations=2" in r


class TestToDataframe:
    def test_dataframe_shape(self, exchange_rate_results):
        pytest.importorskip("pandas")
        rate = ExchangeRate(exchange_rate_results[0])
        df = rate.to_dataframe()
        assert list(df.columns) == ["value"]
        assert df.index.name == "date"
        assert len(df) == 2

    def test_dataframe_values(self, exchange_rate_results):
        pytest.importorskip("pandas")
        rate = ExchangeRate(exchange_rate_results[0])
        df = rate.to_dataframe()
        assert df["value"].tolist() == [141.75, 144.62]
