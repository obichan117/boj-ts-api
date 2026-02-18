"""Tests for the Currency enum and detection functions."""

from __future__ import annotations

from boj_ts_api import SeriesResult
from pyboj._domains.exchange_rate import (
    Currency,
    ExchangeRate,
    RateType,
    _detect_currency,
    _detect_rate_type,
)


class TestCurrencyEnum:
    def test_enum_values(self):
        assert Currency.USD_JPY == "USD/JPY"
        assert Currency.EUR_JPY == "EUR/JPY"
        assert len(Currency) == 26

    def test_value(self):
        assert Currency.USD_JPY.value == "USD/JPY"


class TestDetectCurrency:
    def test_usd(self):
        assert _detect_currency("U.S.dollar/Yen Spot Rate at 9 A.M.") == Currency.USD_JPY

    def test_eur(self):
        assert _detect_currency("Euro/Yen Central Rate") == Currency.EUR_JPY

    def test_gbp(self):
        assert _detect_currency("U.K.pound/Yen Rate") == Currency.GBP_JPY

    def test_unknown(self):
        assert _detect_currency("Unknown currency Rate") is None

    def test_empty(self):
        assert _detect_currency("") is None


class TestDetectRateType:
    def test_spot_9am(self):
        assert _detect_rate_type("Spot Rate at 9 A.M.") == RateType.SPOT_9AM

    def test_central(self):
        assert _detect_rate_type("Central Rate") == RateType.CENTRAL

    def test_other(self):
        assert _detect_rate_type("Unknown metric") == RateType.OTHER


class TestCurrencyPropertyReturnsEnum:
    def test_returns_currency_enum(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "FXERD01",
            "NAME_OF_TIME_SERIES": "U.S.dollar/Yen Spot Rate at 9 A.M.",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = ExchangeRate(result)
        pair = rate.currency_pair
        assert isinstance(pair, Currency)
        assert pair is Currency.USD_JPY
