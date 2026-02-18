"""Tests for pyboj._domains.interest_rate."""

from __future__ import annotations

import datetime

from boj_ts_api import SeriesResult
from pyboj._domains.interest_rate import (
    Collateralization,
    InterestRate,
    RateCategory,
)


class TestInterestRate:
    def test_series_code(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        assert rate.series_code == "STRDCLUCON"

    def test_dates(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        assert rate.dates == [datetime.date(2024, 1, 4), datetime.date(2024, 1, 5)]

    def test_values(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        assert rate.values == [-0.003, -0.002]


class TestRateCategory:
    def test_call_rate(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        assert rate.rate_category == RateCategory.CALL_RATE

    def test_policy_rate(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[2])
        assert rate.rate_category == RateCategory.POLICY_RATE

    def test_unknown_category(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST01",
            "NAME_OF_TIME_SERIES": "Some obscure rate",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = InterestRate(result)
        assert rate.rate_category == RateCategory.OTHER


class TestCollateralization:
    def test_uncollateralized(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        assert rate.collateralization == Collateralization.UNCOLLATERALIZED

    def test_collateralized(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[1])
        assert rate.collateralization == Collateralization.COLLATERALIZED

    def test_not_applicable(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[2])
        assert rate.collateralization is None


class TestTenor:
    def test_overnight_from_name(self, interest_rate_results):
        # "Call Rate, Uncollateralized Overnight"
        rate = InterestRate(interest_rate_results[0])
        assert rate.tenor == "Overnight"

    def test_no_tenor(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST01",
            "NAME_OF_TIME_SERIES": "Basic Discount Rate",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = InterestRate(result)
        assert rate.tenor is None

    def test_numeric_tenor(self):
        result = SeriesResult.model_validate({
            "SERIES_CODE": "TEST02",
            "NAME_OF_TIME_SERIES": "CD Rate 3 Months",
            "VALUES": {"SURVEY_DATES": [], "VALUES": []},
        })
        rate = InterestRate(result)
        assert rate.tenor == "3 Months"


class TestRepr:
    def test_repr_format(self, interest_rate_results):
        rate = InterestRate(interest_rate_results[0])
        r = repr(rate)
        assert "InterestRate" in r
        assert "STRDCLUCON" in r
