"""Price index domain wrapper (PR01-PR04 databases)."""

from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

from pyboj._domains._base import _DomainSeries

if TYPE_CHECKING:
    from boj_ts_api import SeriesResult


class IndexType(str, Enum):
    """High-level classification of the price index."""

    PRODUCER = "producer"
    SERVICES = "services"
    INPUT_OUTPUT = "input_output"
    EXPORT = "export"
    IMPORT = "import"
    FINAL_DEMAND = "final_demand"
    INTERMEDIATE_DEMAND = "intermediate_demand"
    OTHER = "other"


# Ordered list of (pattern, IndexType) — first match wins
_INDEX_TYPE_PATTERNS: list[tuple[str, IndexType]] = [
    (r"[Ee]xport", IndexType.EXPORT),
    (r"[Ii]mport", IndexType.IMPORT),
    (r"[Ii]nput.*[Oo]utput", IndexType.INPUT_OUTPUT),
    (r"[Ff]inal.*[Dd]emand", IndexType.FINAL_DEMAND),
    (r"[Ii]ntermediate.*[Dd]emand", IndexType.INTERMEDIATE_DEMAND),
    (r"[Ss]ervice", IndexType.SERVICES),
    (r"[Pp]roducer|[Cc]orporate.*[Gg]oods|CGPI", IndexType.PRODUCER),
]

# Extract base year from unit strings like "CY2020 average=100"
_BASE_YEAR_RE = re.compile(r"((?:CY|FY)\d{4})")


def _detect_index_type(name: str, category: str) -> IndexType:
    """Detect the index type from a BOJ series name and category."""
    for text in (name, category):
        for pattern, it in _INDEX_TYPE_PATTERNS:
            if re.search(pattern, text):
                return it
    return IndexType.OTHER


class PriceIndex(_DomainSeries):
    """Domain wrapper for price index series (PR01-PR04)."""

    def __init__(self, result: SeriesResult) -> None:
        super().__init__(result)

    @property
    def index_type(self) -> IndexType:
        """Classified index type based on the English series name and category."""
        return _detect_index_type(self.name or "", self.category or "")

    @property
    def base_year(self) -> str | None:
        """Base year string (e.g. ``"CY2020"``) extracted from the unit, or ``None``."""
        unit = self.unit or ""
        m = _BASE_YEAR_RE.search(unit)
        return m.group(1) if m else None

    @property
    def is_yoy_change(self) -> bool:
        """``True`` when the series represents year-on-year percentage change."""
        unit = self.unit or ""
        return "%" in unit and "=100" not in unit
