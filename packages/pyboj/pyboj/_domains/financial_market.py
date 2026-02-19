"""Financial markets domain wrapper (FM03-FM07 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class MarketSegment(str, Enum):
    """Financial market segment classification."""

    SHORT_TERM_MONEY = "short_term_money"
    CALL_MONEY = "call_money"
    CORPORATE_BONDS = "corporate_bonds"
    GOVT_BONDS = "govt_bonds"
    REPO = "repo"
    CP = "cp"
    CD = "cd"
    TB = "tb"
    OTHER = "other"


class InstrumentType(str, Enum):
    """Financial instrument classification."""

    OUTSTANDING = "outstanding"
    ISSUANCE = "issuance"
    TRADING_VOLUME = "trading_volume"
    YIELD = "yield"
    SPREAD = "spread"
    OTHER = "other"


_SEGMENT_PATTERNS: list[tuple[str, MarketSegment]] = [
    (r"[Cc]all\s*[Mm]oney", MarketSegment.CALL_MONEY),
    (r"[Rr]epo|[Gg]ensaki", MarketSegment.REPO),
    (r"[Cc]ommercial\s*[Pp]aper|\bCP\b", MarketSegment.CP),
    (r"[Cc]ertificate.*[Dd]eposit|\bCD\b", MarketSegment.CD),
    (r"[Tt]reasury.*[Bb]ill|\bTB\b|\bT-[Bb]ill", MarketSegment.TB),
    (r"[Cc]orporate.*[Bb]ond|[Dd]ebenture", MarketSegment.CORPORATE_BONDS),
    (r"[Gg]overnment.*[Bb]ond|JGB|[Gg]ovt.*[Bb]ond", MarketSegment.GOVT_BONDS),
    (r"[Ss]hort.*[Tt]erm|[Mm]oney\s*[Mm]arket", MarketSegment.SHORT_TERM_MONEY),
]

_INSTRUMENT_PATTERNS: list[tuple[str, InstrumentType]] = [
    (r"[Oo]utstanding|[Aa]mount|[Bb]alance", InstrumentType.OUTSTANDING),
    (r"[Ii]ssu(?:ance|ed)", InstrumentType.ISSUANCE),
    (r"[Tt]rading.*[Vv]olume|[Tt]urnover|[Tt]ransaction", InstrumentType.TRADING_VOLUME),
    (r"[Ss]pread", InstrumentType.SPREAD),
    (r"[Yy]ield|[Rr]ate", InstrumentType.YIELD),
]


def _detect_segment(name: str) -> MarketSegment:
    """Detect the market segment from a BOJ series name."""
    for pattern, seg in _SEGMENT_PATTERNS:
        if re.search(pattern, name):
            return seg
    return MarketSegment.OTHER


def _detect_instrument(name: str) -> InstrumentType:
    """Detect the instrument type from a BOJ series name."""
    for pattern, inst in _INSTRUMENT_PATTERNS:
        if re.search(pattern, name):
            return inst
    return InstrumentType.OTHER


class FinancialMarket(Series):
    """Domain wrapper for financial markets series (FM03-FM07)."""

    @property
    def segment(self) -> MarketSegment:
        """Detected market segment."""
        return _detect_segment(self.name or "")

    @property
    def instrument_type(self) -> InstrumentType:
        """Detected instrument type."""
        return _detect_instrument(self.name or "")
