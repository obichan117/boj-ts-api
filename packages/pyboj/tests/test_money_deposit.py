"""Tests for the Money/Deposit domain wrapper."""

from __future__ import annotations

from boj_ts_api import SeriesResult
from pyboj._domains.money_deposit import (
    Adjustment,
    MonetaryComponent,
    MoneyDeposit,
    _detect_adjustment,
    _detect_component,
)


class TestMonetaryComponent:
    def test_total(self):
        assert _detect_component("Monetary Base, Total") == MonetaryComponent.TOTAL

    def test_banknotes(self):
        assert _detect_component("Banknotes in Circulation") == MonetaryComponent.BANKNOTES

    def test_coins(self):
        assert _detect_component("Coins in Circulation") == MonetaryComponent.COINS

    def test_current_account(self):
        assert _detect_component("Current Account Balances") == MonetaryComponent.CURRENT_ACCOUNT

    def test_reserve(self):
        assert _detect_component("Reserve Balances") == MonetaryComponent.RESERVE

    def test_m1(self):
        assert _detect_component("M1 (Average)") == MonetaryComponent.M1

    def test_m2(self):
        assert _detect_component("M2 (Average)") == MonetaryComponent.M2

    def test_m3(self):
        assert _detect_component("M3 (Average)") == MonetaryComponent.M3

    def test_broadly_defined(self):
        result = _detect_component("Broadly-defined Liquidity")
        assert result == MonetaryComponent.BROADLY_DEFINED_LIQUIDITY

    def test_other(self):
        assert _detect_component("Unknown Metric") == MonetaryComponent.OTHER


class TestAdjustment:
    def test_nominal(self):
        assert _detect_adjustment("Monetary Base, Total") == Adjustment.NOMINAL

    def test_yoy(self):
        assert _detect_adjustment("Year-on-Year change") == Adjustment.YOY

    def test_seasonally_adjusted(self):
        assert _detect_adjustment("Seasonally Adjusted") == Adjustment.SEASONALLY_ADJUSTED


class TestMoneyDepositWrapper:
    def test_component(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "MD01_TEST",
            "NAME_OF_TIME_SERIES": "Monetary Base, Total",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [650000.0]},
        })
        md = MoneyDeposit(result)
        assert md.component == MonetaryComponent.TOTAL

    def test_adjustment(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "MD01_TEST",
            "NAME_OF_TIME_SERIES": "Monetary Base, Year-on-Year change",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [2.3]},
        })
        md = MoneyDeposit(result)
        assert md.adjustment == Adjustment.YOY

    def test_repr(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "MD01_TEST",
            "NAME_OF_TIME_SERIES": "Monetary Base, Total",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [650000.0]},
        })
        md = MoneyDeposit(result)
        assert "MoneyDeposit" in repr(md)
