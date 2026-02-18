"""Exchange rate domain wrapper (FM08, FM09 databases)."""

from __future__ import annotations

import re
from enum import Enum

from pyboj._domains._base import Series


class Currency(str, Enum):
    """ISO currency pair for exchange rate series."""

    USD_JPY = "USD/JPY"
    EUR_JPY = "EUR/JPY"
    GBP_JPY = "GBP/JPY"
    CHF_JPY = "CHF/JPY"
    SEK_JPY = "SEK/JPY"
    NOK_JPY = "NOK/JPY"
    DKK_JPY = "DKK/JPY"
    CAD_JPY = "CAD/JPY"
    AUD_JPY = "AUD/JPY"
    NZD_JPY = "NZD/JPY"
    ZAR_JPY = "ZAR/JPY"
    KRW_JPY = "KRW/JPY"
    CNY_JPY = "CNY/JPY"
    SGD_JPY = "SGD/JPY"
    THB_JPY = "THB/JPY"
    HKD_JPY = "HKD/JPY"
    TWD_JPY = "TWD/JPY"
    MYR_JPY = "MYR/JPY"
    IDR_JPY = "IDR/JPY"
    PHP_JPY = "PHP/JPY"
    INR_JPY = "INR/JPY"
    MXN_JPY = "MXN/JPY"
    BRL_JPY = "BRL/JPY"
    RUB_JPY = "RUB/JPY"
    SAR_JPY = "SAR/JPY"
    TRY_JPY = "TRY/JPY"


class RateType(str, Enum):
    """Type of exchange rate observation."""

    SPOT_9AM = "spot_9am"
    SPOT_17PM = "spot_17pm"
    CENTRAL = "central"
    HIGHEST = "highest"
    LOWEST = "lowest"
    TURNOVER_SPOT = "turnover_spot"
    TURNOVER_SWAP = "turnover_swap"
    FORWARD_SPREAD = "forward_spread"
    OPTION_VOLATILITY = "option_volatility"
    END_OF_MONTH = "end_of_month"
    AVERAGE = "average"
    NOMINAL_EFFECTIVE = "nominal_effective"
    REAL_EFFECTIVE = "real_effective"
    OTHER = "other"


# BOJ English name fragments → Currency enum (case-insensitive lookup)
_CURRENCY_MAP: dict[str, Currency] = {
    "u.s.dollar": Currency.USD_JPY,
    "us.dollar": Currency.USD_JPY,
    "euro": Currency.EUR_JPY,
    "u.k.pound": Currency.GBP_JPY,
    "swiss franc": Currency.CHF_JPY,
    "swedish krona": Currency.SEK_JPY,
    "norwegian krone": Currency.NOK_JPY,
    "danish krone": Currency.DKK_JPY,
    "canadian dollar": Currency.CAD_JPY,
    "australian dollar": Currency.AUD_JPY,
    "nz dollar": Currency.NZD_JPY,
    "south african rand": Currency.ZAR_JPY,
    "korean won": Currency.KRW_JPY,
    "chinese yuan": Currency.CNY_JPY,
    "singapore dollar": Currency.SGD_JPY,
    "thai baht": Currency.THB_JPY,
    "hong kong dollar": Currency.HKD_JPY,
    "taiwan dollar": Currency.TWD_JPY,
    "malaysian ringgit": Currency.MYR_JPY,
    "indonesian rupiah": Currency.IDR_JPY,
    "philippine peso": Currency.PHP_JPY,
    "indian rupee": Currency.INR_JPY,
    "mexican peso": Currency.MXN_JPY,
    "brazilian real": Currency.BRL_JPY,
    "russian ruble": Currency.RUB_JPY,
    "saudi riyal": Currency.SAR_JPY,
    "turkish lira": Currency.TRY_JPY,
}

# Ordered list of (pattern, RateType) — first match wins
_RATE_TYPE_PATTERNS: list[tuple[str, RateType]] = [
    (r"Spot.*9\s*[Aa]\.?[Mm]", RateType.SPOT_9AM),
    (r"Spot.*17\s*[Pp]\.?[Mm]", RateType.SPOT_17PM),
    (r"Spot.*[Tt]urnover", RateType.TURNOVER_SPOT),
    (r"[Ss]wap.*[Tt]urnover", RateType.TURNOVER_SWAP),
    (r"[Tt]urnover.*[Ss]pot", RateType.TURNOVER_SPOT),
    (r"[Tt]urnover.*[Ss]wap", RateType.TURNOVER_SWAP),
    (r"[Ff]orward.*[Ss]pread", RateType.FORWARD_SPREAD),
    (r"[Oo]ption.*[Vv]olatility", RateType.OPTION_VOLATILITY),
    (r"[Cc]entral", RateType.CENTRAL),
    (r"[Hh]ighest", RateType.HIGHEST),
    (r"[Ll]owest", RateType.LOWEST),
    (r"[Ee]nd.*[Mm]onth", RateType.END_OF_MONTH),
    (r"[Nn]ominal.*[Ee]ffective", RateType.NOMINAL_EFFECTIVE),
    (r"[Rr]eal.*[Ee]ffective", RateType.REAL_EFFECTIVE),
    (r"[Aa]verage", RateType.AVERAGE),
]


def _detect_currency(name: str) -> Currency | None:
    """Detect the currency pair from a BOJ series name."""
    lower = name.lower()
    for fragment, currency in _CURRENCY_MAP.items():
        if fragment in lower:
            return currency
    return None


def _detect_rate_type(name: str) -> RateType:
    """Detect the rate type from a BOJ series name."""
    for pattern, rt in _RATE_TYPE_PATTERNS:
        if re.search(pattern, name):
            return rt
    return RateType.OTHER


class ExchangeRate(Series):
    """Domain wrapper for exchange rate series (FM08 / FM09)."""

    @property
    def currency_pair(self) -> Currency | None:
        """ISO currency pair (e.g. ``Currency.USD_JPY``) or ``None``."""
        return _detect_currency(self.name or "")

    @property
    def rate_type(self) -> RateType:
        """Classified rate type based on the English series name."""
        return _detect_rate_type(self.name or "")
