"""TANKAN survey domain wrapper (CO database)."""

from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

from pyboj._domains._base import Series

if TYPE_CHECKING:
    from boj_ts_api import MetadataRecord


class TankanIndustry(str, Enum):
    """TANKAN industry classification."""

    ALL_INDUSTRIES = "all_industries"
    MANUFACTURING = "manufacturing"
    NON_MANUFACTURING = "non_manufacturing"
    CONSTRUCTION = "construction"
    REAL_ESTATE = "real_estate"
    RETAIL = "retail"
    WHOLESALE = "wholesale"
    TRANSPORT = "transport"
    INFORMATION = "information"
    SERVICES = "services"
    FOOD_BEVERAGES = "food_beverages"
    TEXTILES = "textiles"
    LUMBER_WOOD = "lumber_wood"
    PAPER_PULP = "paper_pulp"
    CHEMICALS = "chemicals"
    PETROLEUM_COAL = "petroleum_coal"
    CERAMICS = "ceramics"
    IRON_STEEL = "iron_steel"
    NONFERROUS_METALS = "nonferrous_metals"
    GENERAL_MACHINERY = "general_machinery"
    ELECTRICAL_MACHINERY = "electrical_machinery"
    MOTOR_VEHICLES = "motor_vehicles"
    SHIPBUILDING = "shipbuilding"
    PRECISION_INSTRUMENTS = "precision_instruments"
    OTHER_MANUFACTURING = "other_manufacturing"
    OTHER = "other"


class TankanSize(str, Enum):
    """TANKAN enterprise size classification."""

    LARGE = "large"
    MEDIUM = "medium"
    SMALL = "small"
    ALL = "all"


class TankanItem(str, Enum):
    """TANKAN survey item."""

    BUSINESS_CONDITIONS = "business_conditions"
    FINANCIAL_POSITION = "financial_position"
    SALES = "sales"
    CURRENT_PROFITS = "current_profits"
    FIXED_INVESTMENT = "fixed_investment"
    EMPLOYMENT = "employment"
    PRODUCTION_CAPACITY = "production_capacity"
    INVENTORY = "inventory"
    SUPPLY_DEMAND = "supply_demand"
    INPUT_PRICES = "input_prices"
    OUTPUT_PRICES = "output_prices"
    OTHER = "other"


class TankanSeriesType(str, Enum):
    """TANKAN series type."""

    DIFFUSION_INDEX = "diffusion_index"
    PERCENT_POINT = "percent_point"
    CHANGE = "change"
    LEVEL = "level"
    OTHER = "other"


class TankanTiming(str, Enum):
    """TANKAN survey timing."""

    ACTUAL = "actual"
    FORECAST = "forecast"


# ── Detection patterns ───────────────────────────────────────────────

_INDUSTRY_PATTERNS: list[tuple[str, TankanIndustry]] = [
    (r"[Aa]ll\s*[Ii]ndustr", TankanIndustry.ALL_INDUSTRIES),
    (r"[Mm]otor\s*[Vv]ehicle", TankanIndustry.MOTOR_VEHICLES),
    (r"[Ee]lectrical\s*[Mm]achinery", TankanIndustry.ELECTRICAL_MACHINERY),
    (r"[Gg]eneral\s*[Mm]achinery", TankanIndustry.GENERAL_MACHINERY),
    (r"[Pp]recision\s*[Ii]nstrument", TankanIndustry.PRECISION_INSTRUMENTS),
    (r"[Ss]hipbuilding", TankanIndustry.SHIPBUILDING),
    (r"[Ff]ood.*[Bb]everage", TankanIndustry.FOOD_BEVERAGES),
    (r"[Tt]extile", TankanIndustry.TEXTILES),
    (r"[Ll]umber|[Ww]ood", TankanIndustry.LUMBER_WOOD),
    (r"[Pp]aper|[Pp]ulp", TankanIndustry.PAPER_PULP),
    (r"[Cc]hemical", TankanIndustry.CHEMICALS),
    (r"[Pp]etroleum|[Cc]oal", TankanIndustry.PETROLEUM_COAL),
    (r"[Cc]eramic", TankanIndustry.CERAMICS),
    (r"[Ii]ron|[Ss]teel", TankanIndustry.IRON_STEEL),
    (r"[Nn]on-?[Ff]errous", TankanIndustry.NONFERROUS_METALS),
    (r"[Nn]on-?[Mm]anufacturing", TankanIndustry.NON_MANUFACTURING),
    (r"[Mm]anufacturing", TankanIndustry.MANUFACTURING),
    (r"[Cc]onstruction", TankanIndustry.CONSTRUCTION),
    (r"[Rr]eal\s*[Ee]state", TankanIndustry.REAL_ESTATE),
    (r"[Rr]etail", TankanIndustry.RETAIL),
    (r"[Ww]holesale", TankanIndustry.WHOLESALE),
    (r"[Tt]ransport", TankanIndustry.TRANSPORT),
    (r"[Ii]nformation", TankanIndustry.INFORMATION),
    (r"[Ss]ervice", TankanIndustry.SERVICES),
]

_SIZE_PATTERNS: list[tuple[str, TankanSize]] = [
    (r"[Ll]arge", TankanSize.LARGE),
    (r"[Mm]edium", TankanSize.MEDIUM),
    (r"[Ss]mall", TankanSize.SMALL),
    (r"[Aa]ll\s*[Ee]nterprise|[Aa]ll\s*[Ss]ize", TankanSize.ALL),
]

_ITEM_PATTERNS: list[tuple[str, TankanItem]] = [
    (r"[Bb]usiness\s*[Cc]ondition", TankanItem.BUSINESS_CONDITIONS),
    (r"[Ff]inancial\s*[Pp]osition", TankanItem.FINANCIAL_POSITION),
    (r"[Cc]urrent\s*[Pp]rofit", TankanItem.CURRENT_PROFITS),
    (r"[Ff]ixed\s*[Ii]nvestment", TankanItem.FIXED_INVESTMENT),
    (r"[Ee]mployment", TankanItem.EMPLOYMENT),
    (r"[Pp]roduction\s*[Cc]apacity", TankanItem.PRODUCTION_CAPACITY),
    (r"[Ii]nventory", TankanItem.INVENTORY),
    (r"[Ss]upply.*[Dd]emand", TankanItem.SUPPLY_DEMAND),
    (r"[Ii]nput\s*[Pp]rice", TankanItem.INPUT_PRICES),
    (r"[Oo]utput\s*[Pp]rice", TankanItem.OUTPUT_PRICES),
    (r"\b[Ss]ales\b", TankanItem.SALES),
]

_SERIES_TYPE_PATTERNS: list[tuple[str, TankanSeriesType]] = [
    (r"[Dd]iffusion\s*[Ii]ndex|D\.?I\.?\b", TankanSeriesType.DIFFUSION_INDEX),
    (r"[Pp]ercent.*[Pp]oint|%\s*point", TankanSeriesType.PERCENT_POINT),
    (r"[Cc]hange|[Cc]hg", TankanSeriesType.CHANGE),
    (r"[Ll]evel", TankanSeriesType.LEVEL),
]


def _detect_tankan_industry(name: str) -> TankanIndustry:
    for pattern, ind in _INDUSTRY_PATTERNS:
        if re.search(pattern, name):
            return ind
    return TankanIndustry.OTHER


def _detect_tankan_size(name: str) -> TankanSize | None:
    for pattern, sz in _SIZE_PATTERNS:
        if re.search(pattern, name):
            return sz
    return None


def _detect_tankan_item(name: str) -> TankanItem:
    for pattern, it in _ITEM_PATTERNS:
        if re.search(pattern, name):
            return it
    return TankanItem.OTHER


def _detect_tankan_series_type(name: str) -> TankanSeriesType:
    for pattern, st in _SERIES_TYPE_PATTERNS:
        if re.search(pattern, name):
            return st
    return TankanSeriesType.OTHER


def _detect_tankan_timing(name: str) -> TankanTiming:
    lower = name.lower()
    if "forecast" in lower or "prospective" in lower:
        return TankanTiming.FORECAST
    return TankanTiming.ACTUAL


def _matches_tankan_filters(
    rec: MetadataRecord,
    *,
    industry: TankanIndustry | None,
    size: TankanSize | None,
    item: TankanItem | None,
    series_type: TankanSeriesType | None,
    timing: TankanTiming | None,
) -> bool:
    """Check if a metadata record matches the requested TANKAN filters."""
    name = rec.NAME_OF_TIME_SERIES or ""
    if industry is not None and _detect_tankan_industry(name) != industry:
        return False
    if size is not None and _detect_tankan_size(name) != size:
        return False
    if item is not None and _detect_tankan_item(name) != item:
        return False
    if series_type is not None and _detect_tankan_series_type(name) != series_type:
        return False
    return timing is None or _detect_tankan_timing(name) == timing


class Tankan(Series):
    """Domain wrapper for TANKAN survey series (CO database)."""

    @property
    def industry(self) -> TankanIndustry:
        """Detected industry classification."""
        return _detect_tankan_industry(self.name or "")

    @property
    def size(self) -> TankanSize | None:
        """Detected enterprise size, or ``None`` if not identifiable."""
        return _detect_tankan_size(self.name or "")

    @property
    def item(self) -> TankanItem:
        """Detected survey item."""
        return _detect_tankan_item(self.name or "")

    @property
    def series_type(self) -> TankanSeriesType:
        """Detected series type (DI, percent point, etc.)."""
        return _detect_tankan_series_type(self.name or "")

    @property
    def timing(self) -> TankanTiming:
        """Detected timing (actual vs forecast)."""
        return _detect_tankan_timing(self.name or "")
