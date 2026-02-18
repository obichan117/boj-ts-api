"""Base class for domain wrapper objects."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pyboj._parsing.dates import parse_survey_dates

if TYPE_CHECKING:
    from boj_ts_api import SeriesResult


class _DomainSeries:
    """Shared functionality for domain wrapper objects.

    Wraps a :class:`~boj_ts_api.SeriesResult` and provides parsed
    dates, cleaned numeric values, and optional DataFrame conversion.
    """

    __slots__ = ("_result",)

    def __init__(self, result: SeriesResult) -> None:
        self._result = result

    # ── Pass-through properties ───────────────────────────────────────

    @property
    def series_code(self) -> str:
        return self._result.SERIES_CODE

    @property
    def name(self) -> str | None:
        """English series name."""
        return self._result.NAME_OF_TIME_SERIES

    @property
    def name_jp(self) -> str | None:
        """Japanese series name."""
        return self._result.NAME_OF_TIME_SERIES_J

    @property
    def unit(self) -> str | None:
        return self._result.UNIT

    @property
    def unit_jp(self) -> str | None:
        return self._result.UNIT_J

    @property
    def frequency(self) -> str | None:
        return self._result.FREQUENCY

    @property
    def category(self) -> str | None:
        return self._result.CATEGORY

    @property
    def category_jp(self) -> str | None:
        return self._result.CATEGORY_J

    # ── Parsed data ───────────────────────────────────────────────────

    @property
    def dates(self) -> list[datetime.date]:
        """Survey dates parsed into :class:`datetime.date` objects."""
        return parse_survey_dates(self._result.VALUES.SURVEY_DATES)

    @property
    def values(self) -> list[float | None]:
        """Numeric values with non-numeric entries converted to ``None``."""
        out: list[float | None] = []
        for v in self._result.VALUES.VALUES:
            if v is None or isinstance(v, str):
                out.append(None)
            else:
                out.append(float(v))
        return out

    # ── Output ────────────────────────────────────────────────────────

    def to_dataframe(self):
        """Return a :class:`pandas.DataFrame` with a ``DatetimeIndex``.

        Requires pandas (``pip install pyboj[pandas]``).

        Returns
        -------
        pandas.DataFrame
            Single column ``value`` indexed by ``date``.
        """
        try:
            import pandas as pd
        except ImportError as exc:
            raise ImportError(
                "pandas is required for to_dataframe(). "
                "Install it with: pip install pyboj[pandas]"
            ) from exc

        index = pd.DatetimeIndex(self.dates, name="date")
        return pd.DataFrame({"value": self.values}, index=index)

    # ── Display ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        cls = type(self).__name__
        n = len(self._result.VALUES.SURVEY_DATES)
        return f"{cls}(series_code={self.series_code!r}, name={self.name!r}, observations={n})"
