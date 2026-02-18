"""Money and deposit domain wrapper (MD01-MD14 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class MonetaryComponent(str, Enum):
    """Monetary aggregate component."""

    TOTAL = "total"
    BANKNOTES = "banknotes"
    COINS = "coins"
    CURRENT_ACCOUNT = "current_account"
    RESERVE = "reserve"
    M1 = "m1"
    M2 = "m2"
    M3 = "m3"
    BROADLY_DEFINED_LIQUIDITY = "broadly_defined_liquidity"
    OTHER = "other"


class Adjustment(str, Enum):
    """Statistical adjustment type."""

    NOMINAL = "nominal"
    YOY = "yoy"
    SEASONALLY_ADJUSTED = "seasonally_adjusted"


_COMPONENT_PATTERNS: list[tuple[str, MonetaryComponent]] = [
    (r"\bM1\b", MonetaryComponent.M1),
    (r"\bM2\b", MonetaryComponent.M2),
    (r"\bM3\b", MonetaryComponent.M3),
    (r"[Bb]roadly.*[Ll]iquidity", MonetaryComponent.BROADLY_DEFINED_LIQUIDITY),
    (r"[Bb]anknote|[Cc]urrency.*[Cc]irculation", MonetaryComponent.BANKNOTES),
    (r"[Cc]oin", MonetaryComponent.COINS),
    (r"[Cc]urrent\s*[Aa]ccount|[Cc]urrent\s*[Dd]eposit", MonetaryComponent.CURRENT_ACCOUNT),
    (r"[Rr]eserve", MonetaryComponent.RESERVE),
    (r"[Tt]otal|[Mm]onetary\s*[Bb]ase", MonetaryComponent.TOTAL),
]

_ADJUSTMENT_PATTERNS: list[tuple[str, Adjustment]] = [
    (r"[Ss]eason", Adjustment.SEASONALLY_ADJUSTED),
    (r"[Yy]ear.*[Yy]ear|[Yy]o[Yy]|y/y|前年比", Adjustment.YOY),
]


def _detect_component(name: str) -> MonetaryComponent:
    """Detect the monetary component from a BOJ series name."""
    for pattern, comp in _COMPONENT_PATTERNS:
        if re.search(pattern, name):
            return comp
    return MonetaryComponent.OTHER


def _detect_adjustment(name: str) -> Adjustment:
    """Detect the adjustment type from a BOJ series name."""
    for pattern, adj in _ADJUSTMENT_PATTERNS:
        if re.search(pattern, name):
            return adj
    return Adjustment.NOMINAL


class MoneyDeposit(Series):
    """Domain wrapper for money and deposit series (MD01-MD14)."""

    @property
    def component(self) -> MonetaryComponent:
        """Detected monetary component."""
        return _detect_component(self.name or "")

    @property
    def adjustment(self) -> Adjustment:
        """Detected adjustment type."""
        return _detect_adjustment(self.name or "")
