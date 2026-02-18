"""Exchange rate domain wrapper (FM08, FM09 databases)."""

from __future__ import annotations

import re
from enum import Enum
from typing import TYPE_CHECKING

from pyboj._domains._base import _DomainSeries

if TYPE_CHECKING:
    from boj_ts_api import SeriesResult


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


# BOJ English name fragments → ISO currency pair
_CURRENCY_MAP: dict[str, str] = {
    "U.S.dollar": "USD/JPY",
    "US.Dollar": "USD/JPY",
    "Euro": "EUR/JPY",
    "U.K.pound": "GBP/JPY",
    "U.K.Pound": "GBP/JPY",
    "Swiss franc": "CHF/JPY",
    "Swiss Franc": "CHF/JPY",
    "Swedish krona": "SEK/JPY",
    "Swedish Krona": "SEK/JPY",
    "Norwegian krone": "NOK/JPY",
    "Norwegian Krone": "NOK/JPY",
    "Danish krone": "DKK/JPY",
    "Danish Krone": "DKK/JPY",
    "Canadian dollar": "CAD/JPY",
    "Canadian Dollar": "CAD/JPY",
    "Australian dollar": "AUD/JPY",
    "Australian Dollar": "AUD/JPY",
    "NZ dollar": "NZD/JPY",
    "NZ Dollar": "NZD/JPY",
    "South African rand": "ZAR/JPY",
    "South African Rand": "ZAR/JPY",
    "Korean won": "KRW/JPY",
    "Korean Won": "KRW/JPY",
    "Chinese yuan": "CNY/JPY",
    "Chinese Yuan": "CNY/JPY",
    "Singapore dollar": "SGD/JPY",
    "Singapore Dollar": "SGD/JPY",
    "Thai baht": "THB/JPY",
    "Thai Baht": "THB/JPY",
    "Hong Kong dollar": "HKD/JPY",
    "Hong Kong Dollar": "HKD/JPY",
    "Taiwan dollar": "TWD/JPY",
    "Taiwan Dollar": "TWD/JPY",
    "Malaysian ringgit": "MYR/JPY",
    "Malaysian Ringgit": "MYR/JPY",
    "Indonesian rupiah": "IDR/JPY",
    "Indonesian Rupiah": "IDR/JPY",
    "Philippine peso": "PHP/JPY",
    "Philippine Peso": "PHP/JPY",
    "Indian rupee": "INR/JPY",
    "Indian Rupee": "INR/JPY",
    "Mexican peso": "MXN/JPY",
    "Mexican Peso": "MXN/JPY",
    "Brazilian real": "BRL/JPY",
    "Brazilian Real": "BRL/JPY",
    "Russian ruble": "RUB/JPY",
    "Russian Ruble": "RUB/JPY",
    "Saudi riyal": "SAR/JPY",
    "Saudi Riyal": "SAR/JPY",
    "Turkish lira": "TRY/JPY",
    "Turkish Lira": "TRY/JPY",
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


class ExchangeRate(_DomainSeries):
    """Domain wrapper for exchange rate series (FM08 / FM09)."""

    def __init__(self, result: SeriesResult) -> None:
        super().__init__(result)

    @property
    def currency_pair(self) -> str | None:
        """ISO currency pair (e.g. ``"USD/JPY"``) or ``None``."""
        name = self.name or ""
        for fragment, pair in _CURRENCY_MAP.items():
            if fragment in name:
                return pair
        return None

    @property
    def rate_type(self) -> RateType:
        """Classified rate type based on the English series name."""
        name = self.name or ""
        for pattern, rt in _RATE_TYPE_PATTERNS:
            if re.search(pattern, name):
                return rt
        return RateType.OTHER
