"""Shared utility functions for pyboj."""

from __future__ import annotations

from boj_ts_api import Frequency

# Map Frequency enum values to prefix(es) expected in BOJ response FREQUENCY field.
# BOJ returns: DAILY, WEEKLY(MON), MONTHLY, QUARTERLY,
#              SEMIANNUAL(CY), SEMIANNUAL(FY), ANNUAL(CY), ANNUAL(FY)
_FREQUENCY_PREFIX: dict[str, str] = {
    "D": "DAILY",
    "W": "WEEKLY",
    "M": "MONTHLY",
    "Q": "QUARTERLY",
    "CH": "SEMIANNUAL(CY)",
    "FH": "SEMIANNUAL(FY)",
    "CY": "ANNUAL(CY)",
    "FY": "ANNUAL(FY)",
}


def frequency_matches(response_freq: str | None, request_freq: Frequency) -> bool:
    """Check if a BOJ response frequency string matches a requested Frequency.

    The BOJ API returns full frequency names (e.g. ``"DAILY"``,
    ``"WEEKLY(MON)"``) while requests use short codes (``Frequency.D``).
    """
    if response_freq is None:
        return False
    expected = _FREQUENCY_PREFIX.get(request_freq.value, "")
    upper = response_freq.upper()
    # WEEKLY needs prefix match (WEEKLY(MON), WEEKLY(FRI), etc.)
    if request_freq is Frequency.W:
        return upper.startswith("WEEKLY")
    return upper == expected
