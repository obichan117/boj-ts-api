"""Tests for the pyboj plotting module."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest
from boj_ts_api import Lang, SeriesResult, SeriesValues
from pyboj._domains._base import Series
from pyboj._plotting._plot import plot_series, set_default_lang


def _make_series(
    *,
    code: str = "TEST001",
    name: str = "Test Series EN",
    name_jp: str = "テスト系列",
    unit: str = "Yen",
    unit_jp: str = "円",
    dates: list[int] | None = None,
    values: list[float] | None = None,
) -> Series:
    """Build a minimal Series from raw data."""
    if dates is None:
        dates = [20240101, 20240201, 20240301]
    if values is None:
        values = [100.0, 110.0, 105.0]
    sr = SeriesResult(
        SERIES_CODE=code,
        NAME_OF_TIME_SERIES=name,
        NAME_OF_TIME_SERIES_J=name_jp,
        UNIT=unit,
        UNIT_J=unit_jp,
        FREQUENCY="MONTHLY",
        VALUES=SeriesValues(SURVEY_DATES=dates, VALUES=values),
    )
    return Series(sr)


@pytest.fixture(autouse=True)
def _use_agg_backend():
    """Force non-interactive Agg backend and close figures after each test."""
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.use("Agg")
    yield
    plt.close("all")


@pytest.fixture(autouse=True)
def _reset_default_lang():
    """Reset the module-level default lang and font cache after each test."""
    import pyboj._plotting._plot as _plot_mod

    yield
    set_default_lang(Lang.JP)
    _plot_mod._japanese_fonts_loaded = False


class TestPlotSeries:
    def test_single_series_returns_axes(self):
        from matplotlib.axes import Axes

        s = _make_series()
        ax = plot_series(s)
        assert isinstance(ax, Axes)

    def test_single_series_auto_title_jp(self):
        s = _make_series(name_jp="日本語タイトル")
        ax = plot_series(s)
        assert ax.get_title() == "日本語タイトル"

    def test_single_series_auto_ylabel_jp(self):
        s = _make_series(unit_jp="億円")
        ax = plot_series(s)
        assert ax.get_ylabel() == "億円"

    def test_single_series_no_legend(self):
        s = _make_series()
        ax = plot_series(s)
        legend = ax.get_legend()
        assert legend is None

    def test_multiple_series_legend_visible(self):
        s1 = _make_series(code="A", name="Series A", name_jp="系列A")
        s2 = _make_series(code="B", name="Series B", name_jp="系列B")
        ax = plot_series(s1, s2)
        legend = ax.get_legend()
        assert legend is not None
        texts = [t.get_text() for t in legend.get_texts()]
        assert "系列A" in texts
        assert "系列B" in texts

    def test_lang_en_override(self):
        s = _make_series(name="English Title", name_jp="日本語タイトル")
        ax = plot_series(s, lang=Lang.EN)
        assert ax.get_title() == "English Title"

    def test_lang_en_ylabel(self):
        s = _make_series(unit="Yen", unit_jp="円")
        ax = plot_series(s, lang=Lang.EN)
        assert ax.get_ylabel() == "Yen"

    def test_lang_en_does_not_use_jp_name(self):
        """Regression: EN must not fall back to name_jp even when it's set."""
        s = _make_series(name="English Only", name_jp="日本語のみ")
        ax = plot_series(s, lang=Lang.EN)
        assert ax.get_title() == "English Only"
        assert ax.get_ylabel() == "Yen"  # not 円

    def test_custom_title_overrides_auto(self):
        s = _make_series()
        ax = plot_series(s, title="Custom Title")
        assert ax.get_title() == "Custom Title"

    def test_custom_ylabel_overrides_auto(self):
        s = _make_series()
        ax = plot_series(s, ylabel="Custom Unit")
        assert ax.get_ylabel() == "Custom Unit"

    def test_no_series_raises(self):
        with pytest.raises(ValueError, match="At least one Series"):
            plot_series()

    def test_set_default_lang_affects_labels(self):
        set_default_lang(Lang.EN)
        s = _make_series(name="EN Name", name_jp="JP名前")
        ax = plot_series(s)
        assert ax.get_title() == "EN Name"


class TestSeriesPlotMethod:
    def test_delegates_to_plot_series(self):
        s = _make_series()
        ax = s.plot()
        assert ax.get_title() == "テスト系列"

    def test_lang_kwarg_forwarded(self):
        s = _make_series(name="English", name_jp="日本語")
        ax = s.plot(lang=Lang.EN)
        assert ax.get_title() == "English"


class TestNoneValues:
    def test_none_in_values_does_not_raise(self):
        """Series.values can contain None; matplotlib should handle gracefully."""
        s = _make_series(
            dates=[20240101, 20240201, 20240301],
            values=[100.0, None, 105.0],
        )
        ax = plot_series(s)
        lines = ax.get_lines()
        assert len(lines) == 1


class TestMissingMatplotlib:
    def test_import_error_message(self):
        with patch.dict(sys.modules, {"matplotlib": None, "matplotlib.pyplot": None}):
            from importlib import reload

            from pyboj._plotting import _plot

            reload(_plot)
            with pytest.raises(ImportError, match="pip install pyboj\\[plot\\]"):
                _plot._ensure_matplotlib()
            # Restore module
            reload(_plot)
