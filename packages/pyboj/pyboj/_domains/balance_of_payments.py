"""Balance of payments domain wrapper (BP01 database)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class BopAccount(str, Enum):
    """Balance of payments account classification."""

    CURRENT = "current"
    GOODS = "goods"
    SERVICES = "services"
    PRIMARY_INCOME = "primary_income"
    SECONDARY_INCOME = "secondary_income"
    CAPITAL = "capital"
    FINANCIAL = "financial"
    DIRECT_INVESTMENT = "direct_investment"
    PORTFOLIO_INVESTMENT = "portfolio_investment"
    RESERVES = "reserves"
    ERRORS_OMISSIONS = "errors_omissions"
    OTHER = "other"


_BOP_PATTERNS: list[tuple[str, BopAccount]] = [
    (r"[Dd]irect\s*[Ii]nvestment", BopAccount.DIRECT_INVESTMENT),
    (r"[Pp]ortfolio\s*[Ii]nvestment", BopAccount.PORTFOLIO_INVESTMENT),
    (r"[Rr]eserve", BopAccount.RESERVES),
    (r"[Ee]rror.*[Oo]mission", BopAccount.ERRORS_OMISSIONS),
    (r"[Pp]rimary\s*[Ii]ncome", BopAccount.PRIMARY_INCOME),
    (r"[Ss]econdary\s*[Ii]ncome", BopAccount.SECONDARY_INCOME),
    (r"[Cc]apital\s*[Aa]ccount", BopAccount.CAPITAL),
    (r"[Ff]inancial\s*[Aa]ccount", BopAccount.FINANCIAL),
    (r"\b[Gg]oods\b", BopAccount.GOODS),
    (r"\b[Ss]ervices\b", BopAccount.SERVICES),
    (r"[Cc]urrent\s*[Aa]ccount", BopAccount.CURRENT),
]


def _detect_bop_account(name: str) -> BopAccount:
    """Detect the BOP account type from a BOJ series name."""
    for pattern, acct in _BOP_PATTERNS:
        if re.search(pattern, name):
            return acct
    return BopAccount.OTHER


class BalanceOfPayments(Series):
    """Domain wrapper for balance of payments series (BP01)."""

    @property
    def account(self) -> BopAccount:
        """Detected BOP account type."""
        return _detect_bop_account(self.name or "")
