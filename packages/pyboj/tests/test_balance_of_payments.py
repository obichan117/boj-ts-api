"""Tests for the Balance of Payments domain wrapper."""

from __future__ import annotations

from boj_ts_api import SeriesResult
from pyboj._domains.balance_of_payments import (
    BalanceOfPayments,
    BopAccount,
    _detect_bop_account,
)


class TestBopAccount:
    def test_current(self):
        assert _detect_bop_account("Current Account Balance") == BopAccount.CURRENT

    def test_goods(self):
        assert _detect_bop_account("Goods Balance") == BopAccount.GOODS

    def test_services(self):
        assert _detect_bop_account("Services Balance") == BopAccount.SERVICES

    def test_primary_income(self):
        assert _detect_bop_account("Primary Income Balance") == BopAccount.PRIMARY_INCOME

    def test_secondary_income(self):
        assert _detect_bop_account("Secondary Income Balance") == BopAccount.SECONDARY_INCOME

    def test_capital(self):
        assert _detect_bop_account("Capital Account") == BopAccount.CAPITAL

    def test_financial(self):
        assert _detect_bop_account("Financial Account") == BopAccount.FINANCIAL

    def test_direct_investment(self):
        assert _detect_bop_account("Direct Investment") == BopAccount.DIRECT_INVESTMENT

    def test_portfolio_investment(self):
        assert _detect_bop_account("Portfolio Investment") == BopAccount.PORTFOLIO_INVESTMENT

    def test_reserves(self):
        assert _detect_bop_account("Reserve Assets") == BopAccount.RESERVES

    def test_errors_omissions(self):
        assert _detect_bop_account("Errors and Omissions") == BopAccount.ERRORS_OMISSIONS

    def test_other(self):
        assert _detect_bop_account("Unknown") == BopAccount.OTHER


class TestBalanceOfPaymentsWrapper:
    def test_account_property(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "BP01_TEST",
            "NAME_OF_TIME_SERIES": "Current Account Balance",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [1500.0]},
        })
        bop = BalanceOfPayments(result)
        assert bop.account == BopAccount.CURRENT

    def test_repr(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "BP01_TEST",
            "NAME_OF_TIME_SERIES": "Goods Balance",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [200.0]},
        })
        bop = BalanceOfPayments(result)
        assert "BalanceOfPayments" in repr(bop)
