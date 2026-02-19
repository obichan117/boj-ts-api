"""International statistics domain wrapper (BIS, DER, PS01, PS02, OT databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class StatCategory(str, Enum):
    """International statistics category classification."""

    BIS_BANKING = "bis_banking"
    BIS_CREDIT = "bis_credit"
    BIS_DEBT_SECURITIES = "bis_debt_securities"
    DERIVATIVES = "derivatives"
    PAYMENT_SYSTEMS = "payment_systems"
    SETTLEMENT = "settlement"
    CROSS_BORDER = "cross_border"
    OTHER = "other"


_CATEGORY_PATTERNS: list[tuple[str, StatCategory]] = [
    (r"[Dd]erivative|[Oo]ption|[Ff]uture|[Ss]wap", StatCategory.DERIVATIVES),
    (r"[Pp]ayment\s*[Ss]ystem|[Pp]ayment\s*[Ss]ettle", StatCategory.PAYMENT_SYSTEMS),
    (r"[Ss]ettlement\s*[Ff]ail|[Ss]ettlement", StatCategory.SETTLEMENT),
    (r"[Cc]ross.*[Bb]order", StatCategory.CROSS_BORDER),
    (r"[Cc]redit.*BIS|BIS.*[Cc]redit", StatCategory.BIS_CREDIT),
    (r"[Dd]ebt\s*[Ss]ecurit.*BIS|BIS.*[Dd]ebt", StatCategory.BIS_DEBT_SECURITIES),
    (r"BIS|[Ii]nternational\s*[Bb]anking", StatCategory.BIS_BANKING),
]


def _detect_stat_category(name: str) -> StatCategory:
    """Detect the statistics category from a BOJ series name."""
    for pattern, cat in _CATEGORY_PATTERNS:
        if re.search(pattern, name):
            return cat
    return StatCategory.OTHER


class InternationalStat(Series):
    """Domain wrapper for international statistics series (BIS, DER, PS01, PS02, OT)."""

    @property
    def stat_category(self) -> StatCategory:
        """Detected statistics category."""
        return _detect_stat_category(self.name or "")
