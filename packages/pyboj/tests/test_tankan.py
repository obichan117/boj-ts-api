"""Tests for the TANKAN domain wrapper."""

from __future__ import annotations

from boj_ts_api import SeriesResult
from pyboj._domains.tankan import (
    Tankan,
    TankanIndustry,
    TankanItem,
    TankanSeriesType,
    TankanSize,
    TankanTiming,
    _detect_tankan_industry,
    _detect_tankan_item,
    _detect_tankan_series_type,
    _detect_tankan_size,
    _detect_tankan_timing,
)


def _make_tankan(name: str) -> Tankan:
    result = SeriesResult.model_validate({
        "SERIES_CODE": "TK01",
        "NAME_OF_TIME_SERIES": name,
        "FREQUENCY": "QUARTERLY",
        "VALUES": {"SURVEY_DATES": [20240301], "VALUES": [12]},
    })
    return Tankan(result)


class TestTankanIndustry:
    def test_all_industries(self):
        assert _detect_tankan_industry("All Industries") == TankanIndustry.ALL_INDUSTRIES

    def test_manufacturing(self):
        assert _detect_tankan_industry("Manufacturing") == TankanIndustry.MANUFACTURING

    def test_non_manufacturing(self):
        assert _detect_tankan_industry("Non-Manufacturing") == TankanIndustry.NON_MANUFACTURING

    def test_motor_vehicles(self):
        assert _detect_tankan_industry("Motor Vehicles") == TankanIndustry.MOTOR_VEHICLES

    def test_other(self):
        assert _detect_tankan_industry("Unknown Sector") == TankanIndustry.OTHER


class TestTankanSize:
    def test_large(self):
        assert _detect_tankan_size("Large Enterprises") == TankanSize.LARGE

    def test_medium(self):
        assert _detect_tankan_size("Medium-sized Enterprises") == TankanSize.MEDIUM

    def test_small(self):
        assert _detect_tankan_size("Small Enterprises") == TankanSize.SMALL

    def test_none(self):
        assert _detect_tankan_size("Unknown") is None


class TestTankanItem:
    def test_business_conditions(self):
        assert _detect_tankan_item("Business Conditions DI") == TankanItem.BUSINESS_CONDITIONS

    def test_financial_position(self):
        assert _detect_tankan_item("Financial Position") == TankanItem.FINANCIAL_POSITION

    def test_sales(self):
        assert _detect_tankan_item("Annual Sales") == TankanItem.SALES

    def test_other(self):
        assert _detect_tankan_item("Unknown Item") == TankanItem.OTHER


class TestTankanSeriesType:
    def test_diffusion_index(self):
        assert _detect_tankan_series_type("Diffusion Index") == TankanSeriesType.DIFFUSION_INDEX

    def test_di_abbreviation(self):
        result = _detect_tankan_series_type("Business Conditions DI")
        assert result == TankanSeriesType.DIFFUSION_INDEX

    def test_percent_point(self):
        assert _detect_tankan_series_type("Percent Point Change") == TankanSeriesType.PERCENT_POINT

    def test_other(self):
        assert _detect_tankan_series_type("Unknown") == TankanSeriesType.OTHER


class TestTankanTiming:
    def test_actual(self):
        assert _detect_tankan_timing("Actual Results") == TankanTiming.ACTUAL

    def test_forecast(self):
        assert _detect_tankan_timing("Forecast") == TankanTiming.FORECAST


class TestTankanWrapper:
    def test_industry(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions DI")
        assert t.industry == TankanIndustry.MANUFACTURING

    def test_size(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions DI")
        assert t.size == TankanSize.LARGE

    def test_item(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions DI")
        assert t.item == TankanItem.BUSINESS_CONDITIONS

    def test_series_type(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions DI")
        assert t.series_type == TankanSeriesType.DIFFUSION_INDEX

    def test_timing_actual(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions DI")
        assert t.timing == TankanTiming.ACTUAL

    def test_timing_forecast(self):
        t = _make_tankan("Manufacturing, Large Enterprises, Business Conditions Forecast")
        assert t.timing == TankanTiming.FORECAST

    def test_repr(self):
        t = _make_tankan("Manufacturing, Large Enterprises")
        assert "Tankan" in repr(t)
        assert "TK01" in repr(t)
