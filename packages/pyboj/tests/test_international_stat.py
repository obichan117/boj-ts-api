"""Tests for the international statistics domain wrapper."""

from pyboj._domains.international_stat import (
    StatCategory,
    _detect_stat_category,
)


class TestDetectStatCategory:
    def test_derivatives(self):
        assert _detect_stat_category("OTC Derivative Market") == StatCategory.DERIVATIVES

    def test_options(self):
        assert _detect_stat_category("Option Contracts") == StatCategory.DERIVATIVES

    def test_payment_systems(self):
        assert _detect_stat_category("Payment System Statistics") == StatCategory.PAYMENT_SYSTEMS

    def test_settlement(self):
        assert _detect_stat_category("Settlement Fails") == StatCategory.SETTLEMENT

    def test_cross_border(self):
        assert _detect_stat_category("Cross-Border Transactions") == StatCategory.CROSS_BORDER

    def test_bis_banking(self):
        assert _detect_stat_category("BIS International Banking") == StatCategory.BIS_BANKING

    def test_bis_credit(self):
        assert _detect_stat_category("BIS Credit to Non-Financial") == StatCategory.BIS_CREDIT

    def test_other(self):
        assert _detect_stat_category("Unknown") == StatCategory.OTHER
