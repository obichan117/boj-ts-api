"""Tests for the financial markets domain wrapper."""

from pyboj._domains.financial_market import (
    InstrumentType,
    MarketSegment,
    _detect_instrument,
    _detect_segment,
)


class TestDetectSegment:
    def test_call_money(self):
        assert _detect_segment("Call Money Outstanding") == MarketSegment.CALL_MONEY

    def test_corporate_bonds(self):
        assert _detect_segment("Corporate Bond Yield") == MarketSegment.CORPORATE_BONDS

    def test_govt_bonds(self):
        assert _detect_segment("Government Bond Trading Volume") == MarketSegment.GOVT_BONDS

    def test_cp(self):
        assert _detect_segment("CP Outstanding") == MarketSegment.CP

    def test_cd(self):
        assert _detect_segment("CD Rate 3-Month") == MarketSegment.CD

    def test_tb(self):
        assert _detect_segment("T-Bill Rate") == MarketSegment.TB

    def test_repo(self):
        assert _detect_segment("Repo Rate, Overnight") == MarketSegment.REPO

    def test_short_term_money(self):
        result = _detect_segment("Short-Term Money Market Outstanding")
        assert result == MarketSegment.SHORT_TERM_MONEY

    def test_other(self):
        assert _detect_segment("Unknown Series") == MarketSegment.OTHER


class TestDetectInstrument:
    def test_outstanding(self):
        assert _detect_instrument("Outstanding Amount") == InstrumentType.OUTSTANDING

    def test_issuance(self):
        assert _detect_instrument("Issuance Volume") == InstrumentType.ISSUANCE

    def test_trading_volume(self):
        assert _detect_instrument("Trading Volume") == InstrumentType.TRADING_VOLUME

    def test_yield(self):
        assert _detect_instrument("Yield on 10-Year") == InstrumentType.YIELD

    def test_spread(self):
        assert _detect_instrument("Credit Spread") == InstrumentType.SPREAD

    def test_other(self):
        assert _detect_instrument("Unknown") == InstrumentType.OTHER
