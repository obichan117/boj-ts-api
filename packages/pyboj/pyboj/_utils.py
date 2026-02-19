"""Shared utility functions for pyboj."""

from __future__ import annotations

from boj_ts_api import Frequency

# Map Frequency enum values to expected BOJ response FREQUENCY field values.
# BOJ returns: DAILY, WEEKLY(MON), MONTHLY, QUARTERLY,
#              SEMIANNUAL, SEMIANNUAL(SEP), ANNUAL, ANNUAL(MAR)
# Source: official API manual (https://www.stat-search.boj.or.jp/info/api_manual.pdf)
_FREQUENCY_PREFIX: dict[str, str] = {
    "D": "DAILY",
    "W": "WEEKLY",
    "M": "MONTHLY",
    "Q": "QUARTERLY",
    "CH": "SEMIANNUAL",
    "FH": "SEMIANNUAL(SEP)",
    "CY": "ANNUAL",
    "FY": "ANNUAL(MAR)",
}

# Frequencies that use prefix matching (have parenthesized variants)
_PREFIX_MATCH = frozenset({Frequency.W, Frequency.CH, Frequency.CY})


def frequency_matches(response_freq: str | None, request_freq: Frequency) -> bool:
    """Check if a BOJ response frequency string matches a requested Frequency.

    The BOJ API returns full frequency names (e.g. ``"DAILY"``,
    ``"WEEKLY(MON)"``) while requests use short codes (``Frequency.D``).
    """
    if response_freq is None:
        return False
    expected = _FREQUENCY_PREFIX.get(request_freq.value, "")
    upper = response_freq.upper()
    # WEEKLY, SEMIANNUAL (CH), ANNUAL (CY) use prefix matching to handle
    # parenthesized variants (e.g. WEEKLY(MON), SEMIANNUAL(SEP), ANNUAL(MAR))
    if request_freq in _PREFIX_MATCH:
        return upper.startswith(expected)
    return upper == expected
