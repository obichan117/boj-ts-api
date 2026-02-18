"""Tests for the Loan domain wrapper."""

from __future__ import annotations

from boj_ts_api import SeriesResult
from pyboj._domains.loan import (
    IndustrySector,
    Loan,
    _detect_sector,
)


class TestIndustrySector:
    def test_manufacturing(self):
        assert _detect_sector("Loans to Manufacturing") == IndustrySector.MANUFACTURING

    def test_construction(self):
        assert _detect_sector("Loans to Construction") == IndustrySector.CONSTRUCTION

    def test_real_estate(self):
        assert _detect_sector("Loans to Real Estate") == IndustrySector.REAL_ESTATE

    def test_total(self):
        assert _detect_sector("Total Loans, All Industries") == IndustrySector.TOTAL

    def test_individuals(self):
        assert _detect_sector("Loans to Individuals") == IndustrySector.INDIVIDUALS

    def test_other(self):
        assert _detect_sector("Unknown category") == IndustrySector.OTHER


class TestLoanWrapper:
    def test_sector(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "LA01_TEST",
            "NAME_OF_TIME_SERIES": "Loans to Manufacturing",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [100000.0]},
        })
        loan = Loan(result)
        assert loan.sector == IndustrySector.MANUFACTURING

    def test_repr(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "LA01_TEST",
            "NAME_OF_TIME_SERIES": "Loans to Manufacturing",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [100000.0]},
        })
        loan = Loan(result)
        assert "Loan" in repr(loan)
