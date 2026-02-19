"""Tests for the flow of funds domain wrapper."""

from pyboj._domains.flow_of_funds import (
    FofInstrument,
    FofSector,
    _detect_fof_instrument,
    _detect_fof_sector,
)


class TestDetectSector:
    def test_households(self):
        assert _detect_fof_sector("Household Financial Assets") == FofSector.HOUSEHOLDS

    def test_non_financial_corps(self):
        result = _detect_fof_sector("Non-Financial Corporations")
        assert result == FofSector.NON_FINANCIAL_CORPORATIONS

    def test_financial_institutions(self):
        result = _detect_fof_sector("Financial Institutions, Total")
        assert result == FofSector.FINANCIAL_INSTITUTIONS

    def test_general_government(self):
        assert _detect_fof_sector("General Government") == FofSector.GENERAL_GOVERNMENT

    def test_overseas(self):
        assert _detect_fof_sector("Overseas Sector") == FofSector.OVERSEAS

    def test_rest_of_world(self):
        assert _detect_fof_sector("Rest of the World") == FofSector.OVERSEAS

    def test_total(self):
        assert _detect_fof_sector("Total All Sectors") == FofSector.TOTAL

    def test_other(self):
        assert _detect_fof_sector("Unknown") == FofSector.OTHER


class TestDetectInstrument:
    def test_currency_deposits(self):
        assert _detect_fof_instrument("Currency and Deposits") == FofInstrument.CURRENCY_DEPOSITS

    def test_loans(self):
        assert _detect_fof_instrument("Loans Outstanding") == FofInstrument.LOANS

    def test_debt_securities(self):
        assert _detect_fof_instrument("Debt Securities") == FofInstrument.DEBT_SECURITIES

    def test_equity(self):
        assert _detect_fof_instrument("Equity and Investment Fund Shares") == FofInstrument.EQUITY

    def test_insurance_pension(self):
        result = _detect_fof_instrument("Insurance and Pension Reserves")
        assert result == FofInstrument.INSURANCE_PENSION

    def test_derivatives(self):
        result = _detect_fof_instrument("Financial Derivatives")
        assert result == FofInstrument.FINANCIAL_DERIVATIVES

    def test_other(self):
        assert _detect_fof_instrument("Unknown") == FofInstrument.OTHER
