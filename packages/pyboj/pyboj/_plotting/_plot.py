"""Plotting utilities for pyboj Series objects."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

from boj_ts_api import Lang

if TYPE_CHECKING:
    from pyboj._domains._base import Series

_default_lang: Lang = Lang.JP
_japanese_fonts_loaded: bool = False


def set_default_lang(lang: Lang) -> None:
    """Set the default language for plot labels.

    Called automatically by :class:`~pyboj.BOJ` on initialization so that
    the plotting language matches the client language.
    """
    global _default_lang  # noqa: PLW0603
    _default_lang = lang


def _ensure_matplotlib():
    """Lazy-import matplotlib and return ``plt``."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError(
            "matplotlib is required for plotting. "
            "Install it with: pip install pyboj[plot]"
        ) from None
    return plt


def _ensure_japanese_fonts() -> None:
    """Import japanize_matplotlib if available, warn otherwise.

    Caches the result so font registration only happens once.
    """
    global _japanese_fonts_loaded  # noqa: PLW0603
    if _japanese_fonts_loaded:
        return
    try:
        import japanize_matplotlib  # noqa: F401

        _japanese_fonts_loaded = True
    except ImportError:
        warnings.warn(
            "japanize-matplotlib is not installed; Japanese text may not render correctly. "
            "Install it with: pip install pyboj[plot]",
            stacklevel=3,
        )


def plot_series(
    *series: Series,
    lang: Lang | None = None,
    title: str | None = None,
    ylabel: str | None = None,
    figsize: tuple[float, float] = (10, 4),
    **kwargs: Any,
):
    """Plot one or more Series on a single Axes.

    Parameters
    ----------
    *series:
        One or more :class:`~pyboj.Series` objects to plot.
    lang:
        Language for auto-generated labels.  Defaults to the language set
        by :func:`set_default_lang` (which follows ``BOJ(lang=...)``).
    title:
        Custom chart title.  If ``None`` and a single series is plotted,
        the series name is used.
    ylabel:
        Custom y-axis label.  If ``None`` and a single series is plotted,
        the series unit is used.
    figsize:
        Figure size ``(width, height)`` in inches.
    **kwargs:
        Passed to ``ax.plot()``.

    Returns
    -------
    matplotlib.axes.Axes
    """
    if not series:
        raise ValueError("At least one Series is required")

    plt = _ensure_matplotlib()
    resolved_lang = lang if lang is not None else _default_lang

    if resolved_lang == Lang.JP:
        _ensure_japanese_fonts()

    fig, ax = plt.subplots(figsize=figsize)

    for s in series:
        if resolved_lang == Lang.JP:
            label = s.name_jp or s.name or s.series_code
        else:
            label = s.name or s.series_code
        ax.plot(s.dates, s.values, label=label, **kwargs)

    # Auto labels for single series
    if len(series) == 1:
        s = series[0]
        if title is None:
            title = (s.name_jp or s.name) if resolved_lang == Lang.JP else s.name
        if ylabel is None:
            ylabel = (s.unit_jp or s.unit) if resolved_lang == Lang.JP else s.unit

    if title:
        ax.set_title(title)
    if ylabel:
        ax.set_ylabel(ylabel)

    if len(series) > 1:
        ax.legend()

    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    return ax
