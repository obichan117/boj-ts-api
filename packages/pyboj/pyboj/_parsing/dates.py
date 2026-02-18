"""Convert BOJ integer survey dates to ``datetime.date`` objects."""

from __future__ import annotations

import datetime


def parse_survey_date(raw: int | str) -> datetime.date:
    """Parse a BOJ survey date into a :class:`datetime.date`.

    Supported formats:

    * ``YYYYMMDD`` (8 digits) → exact date
    * ``YYYYMM`` (6 digits) → first day of month
    * ``YYYY`` (4 digits) → first day of year

    .. note::

       Quarterly (``YYYYQQ``) and semi-annual (``YYYYHH``) dates share the
       6-digit format with monthly dates and are parsed as ``YYYYMM``.  This
       gives correct results for Q1/H1 but maps Q2→Feb, Q3→Mar, Q4→Apr and
       H2→Feb instead of their true calendar months.  Proper disambiguation
       requires the series frequency, which is not available here.

    Parameters
    ----------
    raw:
        Integer or string representation of a BOJ survey date.

    Raises
    ------
    ValueError
        If *raw* does not match any supported format.
    """
    s = str(int(raw))  # normalise "20240101" and 20240101
    length = len(s)

    if length == 8:
        return datetime.date(int(s[:4]), int(s[4:6]), int(s[6:8]))
    if length == 6:
        return datetime.date(int(s[:4]), int(s[4:6]), 1)
    if length == 4:
        return datetime.date(int(s[:4]), 1, 1)

    msg = f"Cannot parse survey date: {raw!r} (expected 4, 6, or 8 digits)"
    raise ValueError(msg)


def parse_survey_dates(raw_dates: list[int | str]) -> list[datetime.date]:
    """Parse a list of BOJ survey dates.

    Parameters
    ----------
    raw_dates:
        List of raw survey date values from :pyattr:`SeriesValues.SURVEY_DATES`.
    """
    return [parse_survey_date(d) for d in raw_dates]
