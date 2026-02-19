"""Base class for domain wrapper objects."""

from __future__ import annotations

import datetime
from typing import TYPE_CHECKING

from pyboj._parsing.dates import parse_survey_dates

if TYPE_CHECKING:
    from boj_ts_api import SeriesResult


class Series:
    """Base class for domain wrapper objects.

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
        """Survey dates parsed into :class:`datetime.date` objects.

        Entries where the raw date is ``None`` are excluded, along with their
        corresponding values, to keep dates and values aligned.
        """
        return [d for d, _ in self._aligned_pairs()]

    @property
    def values(self) -> list[float | None]:
        """Numeric values with non-numeric entries converted to ``None``.

        Entries where the corresponding date is ``None`` are excluded.
        """
        return [v for _, v in self._aligned_pairs()]

    def _aligned_pairs(self) -> list[tuple[datetime.date, float | None]]:
        """Return aligned (date, value) pairs, skipping entries with None dates."""
        raw_dates = parse_survey_dates(self._result.VALUES.SURVEY_DATES)
        raw_values = self._result.VALUES.VALUES
        pairs: list[tuple[datetime.date, float | None]] = []
        for d, v in zip(raw_dates, raw_values, strict=False):
            if d is None:
                continue
            if v is None or isinstance(v, str):
                pairs.append((d, None))
            else:
                pairs.append((d, float(v)))
        return pairs

    # ── Output ────────────────────────────────────────────────────────

    def to_dataframe(self):
        """Return a :class:`pandas.DataFrame` with a ``DatetimeIndex``.

        Returns
        -------
        pandas.DataFrame
            Single column ``value`` indexed by ``date``.
        """
        import pandas as pd

        pairs = self._aligned_pairs()
        index = pd.DatetimeIndex([d for d, _ in pairs], name="date")
        return pd.DataFrame({"value": [v for _, v in pairs]}, index=index)

    # ── Plotting ──────────────────────────────────────────────────────

    def plot(
        self,
        *,
        lang=None,
        title: str | None = None,
        ylabel: str | None = None,
        figsize: tuple[float, float] = (10, 4),
        **kwargs,
    ):
        """Plot this series.

        Parameters
        ----------
        lang:
            Language for labels (``Lang.JP`` or ``Lang.EN``).
            Defaults to the language set on the ``BOJ`` client.
        title:
            Custom chart title.
        ylabel:
            Custom y-axis label.
        figsize:
            Figure size ``(width, height)`` in inches.
        **kwargs:
            Passed to ``ax.plot()``.

        Returns
        -------
        matplotlib.axes.Axes
        """
        from pyboj._plotting import plot_series

        return plot_series(self, lang=lang, title=title, ylabel=ylabel, figsize=figsize, **kwargs)

    # ── Display ───────────────────────────────────────────────────────

    def __repr__(self) -> str:
        cls = type(self).__name__
        n = len(self._result.VALUES.SURVEY_DATES)
        return f"{cls}(series_code={self.series_code!r}, name={self.name!r}, observations={n})"
