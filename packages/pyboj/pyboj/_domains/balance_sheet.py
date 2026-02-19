"""Balance sheet domain wrapper (BS01-BS02 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class AccountSide(str, Enum):
    """Balance sheet side classification."""

    ASSETS = "assets"
    LIABILITIES = "liabilities"
    NET_ASSETS = "net_assets"
    OTHER = "other"


class InstitutionType(str, Enum):
    """Financial institution type."""

    BOJ = "boj"
    CITY_BANKS = "city_banks"
    REGIONAL_BANKS = "regional_banks"
    TRUST_BANKS = "trust_banks"
    SHINKIN_BANKS = "shinkin_banks"
    CREDIT_COOPERATIVES = "credit_cooperatives"
    ALL_BANKS = "all_banks"
    OTHER = "other"


_SIDE_PATTERNS: list[tuple[str, AccountSide]] = [
    (r"[Nn]et\s*[Aa]sset|[Cc]apital\s*[Aa]ccount", AccountSide.NET_ASSETS),
    (r"[Aa]sset|[Ll]oan|[Ss]ecurities\s*[Hh]eld|[Cc]ash", AccountSide.ASSETS),
    (r"[Ll]iabilit|[Dd]eposit|[Bb]orrowing|[Bb]anknote", AccountSide.LIABILITIES),
]

_INSTITUTION_PATTERNS: list[tuple[str, InstitutionType]] = [
    (r"[Bb]ank\s*of\s*[Jj]apan|BOJ\b", InstitutionType.BOJ),
    (r"[Cc]ity\s*[Bb]ank", InstitutionType.CITY_BANKS),
    (r"[Rr]egional\s*[Bb]ank", InstitutionType.REGIONAL_BANKS),
    (r"[Tt]rust\s*[Bb]ank", InstitutionType.TRUST_BANKS),
    (r"[Ss]hinkin", InstitutionType.SHINKIN_BANKS),
    (r"[Cc]redit\s*[Cc]ooperative", InstitutionType.CREDIT_COOPERATIVES),
    (r"[Aa]ll\s*[Bb]ank", InstitutionType.ALL_BANKS),
]


def _detect_side(name: str) -> AccountSide:
    """Detect the balance sheet side from a BOJ series name."""
    for pattern, side in _SIDE_PATTERNS:
        if re.search(pattern, name):
            return side
    return AccountSide.OTHER


def _detect_institution(name: str) -> InstitutionType:
    """Detect the institution type from a BOJ series name."""
    for pattern, inst in _INSTITUTION_PATTERNS:
        if re.search(pattern, name):
            return inst
    return InstitutionType.OTHER


class BalanceSheet(Series):
    """Domain wrapper for balance sheet series (BS01-BS02)."""

    @property
    def account_side(self) -> AccountSide:
        """Detected balance sheet side (assets/liabilities)."""
        return _detect_side(self.name or "")

    @property
    def institution_type(self) -> InstitutionType:
        """Detected institution type."""
        return _detect_institution(self.name or "")
