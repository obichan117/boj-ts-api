"""Flow of funds domain wrapper (FF database)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class FofSector(str, Enum):
    """Flow of funds sector classification."""

    HOUSEHOLDS = "households"
    NON_FINANCIAL_CORPORATIONS = "non_financial_corporations"
    FINANCIAL_INSTITUTIONS = "financial_institutions"
    GENERAL_GOVERNMENT = "general_government"
    OVERSEAS = "overseas"
    TOTAL = "total"
    OTHER = "other"


class FofInstrument(str, Enum):
    """Flow of funds financial instrument classification."""

    CURRENCY_DEPOSITS = "currency_deposits"
    LOANS = "loans"
    DEBT_SECURITIES = "debt_securities"
    EQUITY = "equity"
    INSURANCE_PENSION = "insurance_pension"
    FINANCIAL_DERIVATIVES = "financial_derivatives"
    TOTAL = "total"
    OTHER = "other"


_SECTOR_PATTERNS: list[tuple[str, FofSector]] = [
    (r"[Hh]ousehold", FofSector.HOUSEHOLDS),
    (r"[Nn]on.*[Ff]inancial.*[Cc]orp", FofSector.NON_FINANCIAL_CORPORATIONS),
    (r"[Ff]inancial\s*[Ii]nstitution", FofSector.FINANCIAL_INSTITUTIONS),
    (r"[Gg]eneral\s*[Gg]overnment|[Pp]ublic\s*[Ss]ector", FofSector.GENERAL_GOVERNMENT),
    (r"[Oo]verseas|[Rr]est.*[Ww]orld", FofSector.OVERSEAS),
    (r"[Tt]otal|[Aa]ll\s*[Ss]ector", FofSector.TOTAL),
]

_INSTRUMENT_PATTERNS: list[tuple[str, FofInstrument]] = [
    (r"[Cc]urrency.*[Dd]eposit|[Dd]eposit.*[Cc]urrency", FofInstrument.CURRENCY_DEPOSITS),
    (r"\b[Ll]oan", FofInstrument.LOANS),
    (r"[Dd]ebt\s*[Ss]ecurit|[Bb]ond", FofInstrument.DEBT_SECURITIES),
    (r"[Ee]quit|[Ss]hare|[Ss]tock", FofInstrument.EQUITY),
    (r"[Ii]nsurance|[Pp]ension|[Aa]nnuit", FofInstrument.INSURANCE_PENSION),
    (r"[Dd]erivative", FofInstrument.FINANCIAL_DERIVATIVES),
    (r"[Tt]otal\s*[Ff]inancial|[Ff]inancial.*[Aa]sset.*[Tt]otal", FofInstrument.TOTAL),
]


def _detect_fof_sector(name: str) -> FofSector:
    """Detect the sector from a BOJ flow of funds series name."""
    for pattern, sec in _SECTOR_PATTERNS:
        if re.search(pattern, name):
            return sec
    return FofSector.OTHER


def _detect_fof_instrument(name: str) -> FofInstrument:
    """Detect the instrument from a BOJ flow of funds series name."""
    for pattern, inst in _INSTRUMENT_PATTERNS:
        if re.search(pattern, name):
            return inst
    return FofInstrument.OTHER


class FlowOfFunds(Series):
    """Domain wrapper for flow of funds series (FF)."""

    @property
    def sector(self) -> FofSector:
        """Detected economic sector."""
        return _detect_fof_sector(self.name or "")

    @property
    def instrument(self) -> FofInstrument:
        """Detected financial instrument."""
        return _detect_fof_instrument(self.name or "")
