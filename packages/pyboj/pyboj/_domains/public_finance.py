"""Public finance domain wrapper (PF01-PF02 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class FiscalItem(str, Enum):
    """Public finance item classification."""

    RECEIPTS = "receipts"
    PAYMENTS = "payments"
    TAX_REVENUE = "tax_revenue"
    GOVT_BONDS_OUTSTANDING = "govt_bonds_outstanding"
    GOVT_BONDS_ISSUANCE = "govt_bonds_issuance"
    BORROWING = "borrowing"
    BALANCE = "balance"
    OTHER = "other"


_FISCAL_PATTERNS: list[tuple[str, FiscalItem]] = [
    (r"[Tt]ax\s*[Rr]evenue", FiscalItem.TAX_REVENUE),
    (r"[Rr]eceipt", FiscalItem.RECEIPTS),
    (r"[Pp]ayment|[Ee]xpenditure|[Dd]isburse", FiscalItem.PAYMENTS),
    (r"[Oo]utstanding.*[Bb]ond|[Bb]ond.*[Oo]utstanding|[Dd]ebt\s*[Oo]utstanding",
     FiscalItem.GOVT_BONDS_OUTSTANDING),
    (r"[Ii]ssu(?:ance|ed).*[Bb]ond|[Bb]ond.*[Ii]ssu", FiscalItem.GOVT_BONDS_ISSUANCE),
    (r"[Bb]orrowing", FiscalItem.BORROWING),
    (r"[Bb]alance|[Ss]urplus|[Dd]eficit", FiscalItem.BALANCE),
]


def _detect_fiscal_item(name: str) -> FiscalItem:
    """Detect the fiscal item from a BOJ series name."""
    for pattern, item in _FISCAL_PATTERNS:
        if re.search(pattern, name):
            return item
    return FiscalItem.OTHER


class PublicFinance(Series):
    """Domain wrapper for public finance series (PF01-PF02)."""

    @property
    def fiscal_item(self) -> FiscalItem:
        """Detected fiscal item classification."""
        return _detect_fiscal_item(self.name or "")
