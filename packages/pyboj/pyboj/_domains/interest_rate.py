"""Interest rate domain wrapper (FM01, FM02, IR01-IR04 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class RateCategory(str, Enum):
    """High-level classification of the interest rate."""

    CALL_RATE = "call_rate"
    REPO_RATE = "repo_rate"
    CP_YIELD = "cp_yield"
    CD_RATE = "cd_rate"
    DEPOSIT_RATE = "deposit_rate"
    LENDING_RATE = "lending_rate"
    POLICY_RATE = "policy_rate"
    OTHER = "other"


class Collateralization(str, Enum):
    """Whether the rate is collateralized or uncollateralized."""

    COLLATERALIZED = "collateralized"
    UNCOLLATERALIZED = "uncollateralized"


# Ordered list of (pattern, RateCategory) — first match wins
_CATEGORY_PATTERNS: list[tuple[str, RateCategory]] = [
    (r"[Pp]olicy.*[Rr]ate|[Bb]asic.*[Dd]iscount|[Bb]asic.*[Ll]oan", RateCategory.POLICY_RATE),
    (r"[Cc]all\s*[Rr]ate|[Cc]all\s*[Mm]oney", RateCategory.CALL_RATE),
    (r"[Rr]epo|[Gg]ensaki", RateCategory.REPO_RATE),
    (r"[Cc]ommercial\s*[Pp]aper|CP\b", RateCategory.CP_YIELD),
    (r"\bCD\b|[Cc]ertificate.*[Dd]eposit", RateCategory.CD_RATE),
    (r"[Dd]eposit", RateCategory.DEPOSIT_RATE),
    (r"[Ll]oan|[Ll]ending|[Dd]iscount", RateCategory.LENDING_RATE),
]

# Tenor extraction: match common tenor labels in series names
_TENOR_RE = re.compile(
    r"(?P<tenor>"
    r"[Oo]vernight|O/?N"
    r"|[Tt]om(?:orrow)?/?[Nn]ext|T/?N"
    r"|\d+\s*[Yy](?:ear)?s?"
    r"|\d+\s*[Mm](?:onth)?s?"
    r"|\d+\s*[Ww](?:eek)?s?"
    r"|\d+\s*[Dd](?:ay)?s?"
    r")"
)


def _detect_rate_category(name: str) -> RateCategory:
    """Detect the rate category from a BOJ series name."""
    for pattern, cat in _CATEGORY_PATTERNS:
        if re.search(pattern, name):
            return cat
    return RateCategory.OTHER


def _detect_collateralization(name: str) -> Collateralization | None:
    """Detect collateralization type from a BOJ series name."""
    lower = name.lower()
    if "uncollateralized" in lower:
        return Collateralization.UNCOLLATERALIZED
    if "collateralized" in lower:
        return Collateralization.COLLATERALIZED
    return None


class InterestRate(Series):
    """Domain wrapper for interest rate series (FM01, FM02, IR01-IR04)."""

    @property
    def rate_category(self) -> RateCategory:
        """Classified rate category based on the English series name."""
        return _detect_rate_category(self.name or "")

    @property
    def collateralization(self) -> Collateralization | None:
        """Collateralization type, or ``None`` if not applicable."""
        return _detect_collateralization(self.name or "")

    @property
    def tenor(self) -> str | None:
        """Extracted tenor string (e.g. ``"overnight"``, ``"3M"``), or ``None``."""
        name = self.name or ""
        m = _TENOR_RE.search(name)
        if m:
            return m.group("tenor")
        return None
