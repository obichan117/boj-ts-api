"""Tests for the public finance domain wrapper."""

from pyboj._domains.public_finance import (
    FiscalItem,
    _detect_fiscal_item,
)


class TestDetectFiscalItem:
    def test_tax_revenue(self):
        assert _detect_fiscal_item("Tax Revenue") == FiscalItem.TAX_REVENUE

    def test_receipts(self):
        assert _detect_fiscal_item("Total Receipts") == FiscalItem.RECEIPTS

    def test_payments(self):
        assert _detect_fiscal_item("General Expenditure Payments") == FiscalItem.PAYMENTS

    def test_bonds_outstanding(self):
        result = _detect_fiscal_item("Government Bonds Outstanding")
        assert result == FiscalItem.GOVT_BONDS_OUTSTANDING

    def test_debt_outstanding(self):
        result = _detect_fiscal_item("National Debt Outstanding")
        assert result == FiscalItem.GOVT_BONDS_OUTSTANDING

    def test_bonds_issuance(self):
        assert _detect_fiscal_item("Bond Issuance Amount") == FiscalItem.GOVT_BONDS_ISSUANCE

    def test_borrowing(self):
        assert _detect_fiscal_item("Government Borrowing") == FiscalItem.BORROWING

    def test_balance(self):
        assert _detect_fiscal_item("Fiscal Balance") == FiscalItem.BALANCE

    def test_surplus(self):
        assert _detect_fiscal_item("Budget Surplus") == FiscalItem.BALANCE

    def test_other(self):
        assert _detect_fiscal_item("Unknown") == FiscalItem.OTHER
