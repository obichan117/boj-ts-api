"""Loan domain wrapper (LA01-LA05 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class IndustrySector(str, Enum):
    """Industry sector classification for loan data."""

    MANUFACTURING = "manufacturing"
    CONSTRUCTION = "construction"
    REAL_ESTATE = "real_estate"
    RETAIL = "retail"
    WHOLESALE = "wholesale"
    TRANSPORT = "transport"
    INFORMATION = "information"
    ELECTRICITY_GAS = "electricity_gas"
    AGRICULTURE = "agriculture"
    FINANCE_INSURANCE = "finance_insurance"
    GOVERNMENT = "government"
    INDIVIDUALS = "individuals"
    TOTAL = "total"
    OTHER = "other"


_SECTOR_PATTERNS: list[tuple[str, IndustrySector]] = [
    (r"[Mm]anufacturing", IndustrySector.MANUFACTURING),
    (r"[Cc]onstruction", IndustrySector.CONSTRUCTION),
    (r"[Rr]eal\s*[Ee]state", IndustrySector.REAL_ESTATE),
    (r"[Rr]etail", IndustrySector.RETAIL),
    (r"[Ww]holesale", IndustrySector.WHOLESALE),
    (r"[Tt]ransport", IndustrySector.TRANSPORT),
    (r"[Ii]nformation", IndustrySector.INFORMATION),
    (r"[Ee]lectricit|[Gg]as.*[Ww]ater", IndustrySector.ELECTRICITY_GAS),
    (r"[Aa]gricultur|[Ff]orestry|[Ff]ishing", IndustrySector.AGRICULTURE),
    (r"[Ff]inance.*[Ii]nsurance|[Bb]anking", IndustrySector.FINANCE_INSURANCE),
    (r"[Gg]overnment|[Ll]ocal\s*[Pp]ublic", IndustrySector.GOVERNMENT),
    (r"[Ii]ndividual|[Hh]ousehold|[Pp]ersonal", IndustrySector.INDIVIDUALS),
    (r"[Tt]otal|[Aa]ll\s*[Ii]ndustr", IndustrySector.TOTAL),
]


def _detect_sector(name: str) -> IndustrySector:
    """Detect the industry sector from a BOJ series name."""
    for pattern, sec in _SECTOR_PATTERNS:
        if re.search(pattern, name):
            return sec
    return IndustrySector.OTHER


class Loan(Series):
    """Domain wrapper for loan series (LA01-LA05)."""

    @property
    def sector(self) -> IndustrySector:
        """Detected industry sector."""
        return _detect_sector(self.name or "")
