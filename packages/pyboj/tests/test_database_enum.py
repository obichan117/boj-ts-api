"""Tests for pyboj._config.Database enum."""

from __future__ import annotations

from pyboj._config import Database


class TestDatabaseEnum:
    def test_value(self):
        assert Database.EXCHANGE_RATES.value == "FM08"

    def test_is_str_subclass(self):
        assert isinstance(Database.EXCHANGE_RATES, str)

    def test_equality_with_string(self):
        assert Database.EXCHANGE_RATES == "FM08"

    def test_known_codes(self):
        expected = {
            Database.BASIC_DISCOUNT_RATE: "IR01",
            Database.CALL_RATES: "FM01",
            Database.EXCHANGE_RATES: "FM08",
            Database.MONETARY_BASE: "MD01",
            Database.TANKAN: "CO",
            Database.PRODUCER_PRICE_INDEX: "PR01",
            Database.BALANCE_OF_PAYMENTS: "BP01",
            Database.BOJ_ACCOUNTS: "BS01",
            Database.FLOW_OF_FUNDS: "FF",
        }
        for member, code in expected.items():
            assert member.value == code

    def test_all_values_unique(self):
        values = [m.value for m in Database]
        assert len(values) == len(set(values))

    def test_usable_as_dict_key(self):
        d = {Database.EXCHANGE_RATES: "test"}
        assert d["FM08"] == "test"
