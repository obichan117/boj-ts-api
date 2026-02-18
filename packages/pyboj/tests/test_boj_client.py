"""Tests for the high-level BOJ client."""

from __future__ import annotations

import respx
from boj_ts_api._types.config import BASE_URL, ENDPOINT_DATA_CODE, ENDPOINT_METADATA
from pyboj import BOJ, Currency, Database, Frequency, RateType
from pyboj._domains._base import Series
from pyboj._domains.balance_of_payments import BalanceOfPayments, BopAccount
from pyboj._domains.exchange_rate import ExchangeRate
from pyboj._domains.interest_rate import InterestRate, RateCategory
from pyboj._domains.loan import Loan
from pyboj._domains.money_deposit import MoneyDeposit
from pyboj._domains.price_index import IndexType, PriceIndex
from pyboj._domains.tankan import Tankan, TankanIndustry
from pyboj._utils import frequency_matches

# ── Fixture data ─────────────────────────────────────────────────────

METADATA_FM08 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "FM08", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": None,
            "NAME_OF_TIME_SERIES": "Header Row",
            "FREQUENCY": "DAILY",
        },
        {
            "SERIES_CODE": "FXERD01",
            "NAME_OF_TIME_SERIES": "U.S.dollar/Yen Spot Rate at 9 A.M.",
            "FREQUENCY": "DAILY",
            "CATEGORY": "Foreign Exchange Rates",
        },
        {
            "SERIES_CODE": "FXERC01",
            "NAME_OF_TIME_SERIES": "Euro/Yen Central Rate",
            "FREQUENCY": "DAILY",
            "CATEGORY": "Foreign Exchange Rates",
        },
        {
            "SERIES_CODE": "FXERM01",
            "NAME_OF_TIME_SERIES": "U.S.dollar/Yen Average Rate",
            "FREQUENCY": "MONTHLY",
            "CATEGORY": "Foreign Exchange Rates",
        },
    ],
}

DATA_FM08 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "FM08", "code": "FXERD01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "FXERD01",
            "NAME_OF_TIME_SERIES": "U.S.dollar/Yen Spot Rate at 9 A.M.",
            "UNIT": "Yen",
            "FREQUENCY": "DAILY",
            "CATEGORY": "Foreign Exchange Rates",
            "VALUES": {"SURVEY_DATES": [20240104, 20240105], "VALUES": [141.75, 144.62]},
        }
    ],
}

DATA_FM08_MULTI = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "FM08", "code": "FXERD01,FXERC01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "FXERD01",
            "NAME_OF_TIME_SERIES": "U.S.dollar/Yen Spot Rate at 9 A.M.",
            "UNIT": "Yen",
            "FREQUENCY": "DAILY",
            "VALUES": {"SURVEY_DATES": [20240104], "VALUES": [141.75]},
        },
        {
            "SERIES_CODE": "FXERC01",
            "NAME_OF_TIME_SERIES": "Euro/Yen Central Rate",
            "UNIT": "Yen",
            "FREQUENCY": "DAILY",
            "VALUES": {"SURVEY_DATES": [20240104], "VALUES": [155.30]},
        },
    ],
}

METADATA_FM01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "FM01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "STRDCLUCON",
            "NAME_OF_TIME_SERIES": "Call Rate, Uncollateralized Overnight",
            "FREQUENCY": "DAILY",
        },
    ],
}

DATA_FM01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "FM01", "code": "STRDCLUCON", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "STRDCLUCON",
            "NAME_OF_TIME_SERIES": "Call Rate, Uncollateralized Overnight",
            "UNIT": "% per annum",
            "FREQUENCY": "DAILY",
            "VALUES": {"SURVEY_DATES": [20240104], "VALUES": [-0.003]},
        },
    ],
}

METADATA_PR01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "PR01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "PRCG100000",
            "NAME_OF_TIME_SERIES": "Producer Price Index, All commodities",
            "FREQUENCY": "MONTHLY",
            "CATEGORY": "Producer Price Index",
        },
    ],
}

DATA_PR01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "PR01", "code": "PRCG100000", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "PRCG100000",
            "NAME_OF_TIME_SERIES": "Producer Price Index, All commodities",
            "UNIT": "CY2020 average=100",
            "FREQUENCY": "MONTHLY",
            "CATEGORY": "Producer Price Index",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [120.1]},
        },
    ],
}

METADATA_CO = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "CO", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "TK01",
            "NAME_OF_TIME_SERIES": "Manufacturing, Large Enterprises, Business Conditions DI",
            "FREQUENCY": "QUARTERLY",
        },
    ],
}

DATA_CO = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "CO", "code": "TK01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "TK01",
            "NAME_OF_TIME_SERIES": "Manufacturing, Large Enterprises, Business Conditions DI",
            "FREQUENCY": "QUARTERLY",
            "VALUES": {"SURVEY_DATES": [20240301], "VALUES": [12]},
        },
    ],
}

METADATA_BP01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "BP01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "BP01_CA",
            "NAME_OF_TIME_SERIES": "Current Account Balance",
            "FREQUENCY": "MONTHLY",
        },
        {
            "SERIES_CODE": "BP01_G",
            "NAME_OF_TIME_SERIES": "Goods Balance",
            "FREQUENCY": "MONTHLY",
        },
    ],
}

DATA_BP01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "BP01", "code": "BP01_CA", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "BP01_CA",
            "NAME_OF_TIME_SERIES": "Current Account Balance",
            "FREQUENCY": "MONTHLY",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [1500.0]},
        },
    ],
}

METADATA_MD01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "MD01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "MD01_TOTAL",
            "NAME_OF_TIME_SERIES": "Monetary Base, Total",
            "FREQUENCY": "MONTHLY",
        },
    ],
}

DATA_MD01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "MD01", "code": "MD01_TOTAL", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "MD01_TOTAL",
            "NAME_OF_TIME_SERIES": "Monetary Base, Total",
            "FREQUENCY": "MONTHLY",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [650000.0]},
        },
    ],
}

METADATA_LA01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "LA01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "LA01_MFG",
            "NAME_OF_TIME_SERIES": "Loans to Manufacturing",
            "FREQUENCY": "MONTHLY",
        },
    ],
}

DATA_LA01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "LA01", "code": "LA01_MFG", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "LA01_MFG",
            "NAME_OF_TIME_SERIES": "Loans to Manufacturing",
            "FREQUENCY": "MONTHLY",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [100000.0]},
        },
    ],
}

METADATA_BS01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T14:00:00.000+09:00",
    "PARAMETER": {"db": "BS01", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "BS01_A",
            "NAME_OF_TIME_SERIES": "BOJ Account Balance",
            "FREQUENCY": "MONTHLY",
        },
    ],
}

DATA_BS01 = {
    "STATUS": 200,
    "MESSAGEID": "M181000I",
    "MESSAGE": "",
    "DATE": "2025-12-02T13:00:00.000+09:00",
    "PARAMETER": {"db": "BS01", "code": "BS01_A", "format": "json", "lang": "en"},
    "NEXTPOSITION": None,
    "RESULTSET": [
        {
            "SERIES_CODE": "BS01_A",
            "NAME_OF_TIME_SERIES": "BOJ Account Balance",
            "FREQUENCY": "MONTHLY",
            "VALUES": {"SURVEY_DATES": [202401], "VALUES": [5000.0]},
        },
    ],
}


def _mock_metadata(mock, db: str, metadata: dict):
    """Set up a respx mock for metadata endpoint."""
    mock.get(
        BASE_URL + ENDPOINT_METADATA,
        params__contains={"db": db},
    ).respond(json=metadata)


def _mock_data(mock, db: str, data: dict, code: str | None = None):
    """Set up a respx mock for data_code endpoint."""
    params = {"db": db}
    if code:
        params["code"] = code
    mock.get(
        BASE_URL + ENDPOINT_DATA_CODE,
        params__contains=params,
    ).respond(json=data)


# ── Tests ────────────────────────────────────────────────────────────


class TestFrequencyMatches:
    def test_daily(self):
        assert frequency_matches("DAILY", Frequency.D) is True

    def test_weekly(self):
        assert frequency_matches("WEEKLY(MON)", Frequency.W) is True

    def test_weekly_plain(self):
        assert frequency_matches("WEEKLY", Frequency.W) is True

    def test_monthly(self):
        assert frequency_matches("MONTHLY", Frequency.M) is True

    def test_quarterly(self):
        assert frequency_matches("QUARTERLY", Frequency.Q) is True

    def test_annual_cy(self):
        assert frequency_matches("ANNUAL(CY)", Frequency.CY) is True

    def test_annual_fy(self):
        assert frequency_matches("ANNUAL(FY)", Frequency.FY) is True

    def test_mismatch(self):
        assert frequency_matches("DAILY", Frequency.M) is False

    def test_none(self):
        assert frequency_matches(None, Frequency.D) is False

    def test_semiannual_cy(self):
        assert frequency_matches("SEMIANNUAL(CY)", Frequency.CH) is True

    def test_semiannual_fy(self):
        assert frequency_matches("SEMIANNUAL(FY)", Frequency.FH) is True


class TestBOJContextManager:
    @respx.mock
    def test_context_manager(self):
        with BOJ() as boj:
            assert boj._client is not None

    @respx.mock
    def test_close(self):
        boj = BOJ()
        boj.close()


class TestBOJMetadata:
    @respx.mock
    def test_metadata(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        boj = BOJ()
        records = boj.metadata(Database.EXCHANGE_RATES)
        assert len(records) == 4
        boj.close()

    @respx.mock
    def test_metadata_cached(self):
        route = respx.get(
            BASE_URL + ENDPOINT_METADATA,
            params__contains={"db": "FM08"},
        ).respond(json=METADATA_FM08)
        boj = BOJ()
        boj.metadata(Database.EXCHANGE_RATES)
        boj.metadata(Database.EXCHANGE_RATES)
        assert route.call_count == 1
        boj.close()


class TestExchangeRates:
    @respx.mock
    def test_all_daily(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        _mock_data(respx, "FM08", DATA_FM08_MULTI)
        boj = BOJ()
        rates = boj.exchange_rates(frequency=Frequency.D)
        assert len(rates) == 2
        assert all(isinstance(r, ExchangeRate) for r in rates)
        boj.close()

    @respx.mock
    def test_filter_by_currency(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        _mock_data(respx, "FM08", DATA_FM08)
        boj = BOJ()
        rates = boj.exchange_rates(currency=Currency.USD_JPY, frequency=Frequency.D)
        assert len(rates) == 1
        assert rates[0].currency_pair == Currency.USD_JPY
        boj.close()

    @respx.mock
    def test_filter_by_rate_type(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        _mock_data(respx, "FM08", DATA_FM08)
        boj = BOJ()
        rates = boj.exchange_rates(rate_type=RateType.SPOT_9AM, frequency=Frequency.D)
        assert len(rates) == 1
        boj.close()

    @respx.mock
    def test_empty_result(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        boj = BOJ()
        # Filter for something that doesn't match any metadata
        rates = boj.exchange_rates(currency=Currency.BRL_JPY)
        assert rates == []
        boj.close()

    @respx.mock
    def test_frequency_filter(self):
        _mock_metadata(respx, "FM08", METADATA_FM08)
        _mock_data(respx, "FM08", DATA_FM08)
        boj = BOJ()
        # Only FXERM01 has MONTHLY frequency but it's USD average
        rates = boj.exchange_rates(frequency=Frequency.M, currency=Currency.USD_JPY)
        assert len(rates) == 1
        boj.close()


class TestInterestRates:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "FM01", METADATA_FM01)
        _mock_data(respx, "FM01", DATA_FM01)
        boj = BOJ()
        rates = boj.interest_rates()
        assert len(rates) == 1
        assert isinstance(rates[0], InterestRate)
        assert rates[0].rate_category == RateCategory.CALL_RATE
        boj.close()


class TestPriceIndices:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "PR01", METADATA_PR01)
        _mock_data(respx, "PR01", DATA_PR01)
        boj = BOJ()
        indices = boj.price_indices()
        assert len(indices) == 1
        assert isinstance(indices[0], PriceIndex)
        assert indices[0].index_type == IndexType.PRODUCER
        boj.close()


class TestTankan:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "CO", METADATA_CO)
        _mock_data(respx, "CO", DATA_CO)
        boj = BOJ()
        results = boj.tankan()
        assert len(results) == 1
        assert isinstance(results[0], Tankan)
        boj.close()

    @respx.mock
    def test_filter_by_industry(self):
        _mock_metadata(respx, "CO", METADATA_CO)
        _mock_data(respx, "CO", DATA_CO)
        boj = BOJ()
        results = boj.tankan(industry=TankanIndustry.MANUFACTURING)
        assert len(results) == 1
        boj.close()

    @respx.mock
    def test_filter_mismatch(self):
        _mock_metadata(respx, "CO", METADATA_CO)
        boj = BOJ()
        results = boj.tankan(industry=TankanIndustry.CONSTRUCTION)
        assert results == []
        boj.close()


class TestBalanceOfPayments:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "BP01", METADATA_BP01)
        _mock_data(respx, "BP01", DATA_BP01)
        boj = BOJ()
        results = boj.balance_of_payments(account=BopAccount.CURRENT)
        assert len(results) == 1
        assert isinstance(results[0], BalanceOfPayments)
        boj.close()


class TestMoneyDeposits:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "MD01", METADATA_MD01)
        _mock_data(respx, "MD01", DATA_MD01)
        boj = BOJ()
        results = boj.money_deposits()
        assert len(results) == 1
        assert isinstance(results[0], MoneyDeposit)
        boj.close()


class TestLoans:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "LA01", METADATA_LA01)
        _mock_data(respx, "LA01", DATA_LA01)
        boj = BOJ()
        results = boj.loans()
        assert len(results) == 1
        assert isinstance(results[0], Loan)
        boj.close()


class TestLightWrappers:
    @respx.mock
    def test_balance_sheets(self):
        _mock_metadata(respx, "BS01", METADATA_BS01)
        _mock_data(respx, "BS01", DATA_BS01)
        boj = BOJ()
        results = boj.balance_sheets()
        assert len(results) == 1
        assert isinstance(results[0], Series)
        boj.close()
