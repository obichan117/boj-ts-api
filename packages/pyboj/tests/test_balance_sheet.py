"""Tests for the balance sheet domain wrapper."""

from pyboj._domains.balance_sheet import (
    AccountSide,
    InstitutionType,
    _detect_institution,
    _detect_side,
)


class TestDetectSide:
    def test_assets(self):
        assert _detect_side("Total Assets") == AccountSide.ASSETS

    def test_liabilities(self):
        assert _detect_side("Total Liabilities") == AccountSide.LIABILITIES

    def test_net_assets(self):
        assert _detect_side("Net Assets") == AccountSide.NET_ASSETS

    def test_loans_as_asset(self):
        assert _detect_side("Loans and Discounts") == AccountSide.ASSETS

    def test_deposits_as_liability(self):
        assert _detect_side("Deposits") == AccountSide.LIABILITIES

    def test_securities_held(self):
        assert _detect_side("Securities Held") == AccountSide.ASSETS

    def test_banknotes(self):
        assert _detect_side("Banknotes in Circulation") == AccountSide.LIABILITIES

    def test_other(self):
        assert _detect_side("Unknown Series") == AccountSide.OTHER


class TestDetectInstitution:
    def test_boj(self):
        assert _detect_institution("Bank of Japan Account") == InstitutionType.BOJ

    def test_city_banks(self):
        assert _detect_institution("City Bank Deposits") == InstitutionType.CITY_BANKS

    def test_regional_banks(self):
        assert _detect_institution("Regional Bank Loans") == InstitutionType.REGIONAL_BANKS

    def test_trust_banks(self):
        assert _detect_institution("Trust Bank Securities") == InstitutionType.TRUST_BANKS

    def test_shinkin(self):
        assert _detect_institution("Shinkin Banks Total") == InstitutionType.SHINKIN_BANKS

    def test_all_banks(self):
        assert _detect_institution("All Banks Total") == InstitutionType.ALL_BANKS

    def test_other(self):
        assert _detect_institution("Unknown") == InstitutionType.OTHER
