"""Tests for the high-level BOJ client."""

from __future__ import annotations

import respx
from boj_ts_api._types.config import BASE_URL, ENDPOINT_DATA_CODE, ENDPOINT_METADATA
from conftest import _load_json
from pyboj import BOJ, Currency, Database, Frequency, RateType
from pyboj._domains.balance_of_payments import BalanceOfPayments, BopAccount
from pyboj._domains.balance_sheet import BalanceSheet, InstitutionType
from pyboj._domains.boj_operation import BOJOperation
from pyboj._domains.exchange_rate import ExchangeRate
from pyboj._domains.financial_market import FinancialMarket
from pyboj._domains.flow_of_funds import FlowOfFunds
from pyboj._domains.interest_rate import InterestRate, RateCategory
from pyboj._domains.international_stat import InternationalStat
from pyboj._domains.loan import Loan
from pyboj._domains.money_deposit import MoneyDeposit
from pyboj._domains.price_index import IndexType, PriceIndex
from pyboj._domains.public_finance import PublicFinance
from pyboj._domains.tankan import Tankan, TankanIndustry
from pyboj._utils import frequency_matches

# ── Fixture data (loaded from JSON files) ────────────────────────────

METADATA_FM08 = _load_json("metadata_fm08.json")
DATA_FM08 = _load_json("data_fm08.json")
DATA_FM08_MULTI = _load_json("data_fm08_multi.json")
METADATA_FM01 = _load_json("metadata_fm01.json")
DATA_FM01 = _load_json("data_fm01.json")
METADATA_PR01 = _load_json("metadata_pr01.json")
DATA_PR01 = _load_json("data_pr01.json")
METADATA_CO = _load_json("metadata_co.json")
DATA_CO = _load_json("data_co.json")
METADATA_BP01 = _load_json("metadata_bp01.json")
DATA_BP01 = _load_json("data_bp01.json")
METADATA_MD01 = _load_json("metadata_md01.json")
DATA_MD01 = _load_json("data_md01.json")
METADATA_LA01 = _load_json("metadata_la01.json")
DATA_LA01 = _load_json("data_la01.json")
METADATA_BS01 = _load_json("metadata_bs01.json")
DATA_BS01 = _load_json("data_bs01.json")
METADATA_FM03 = _load_json("metadata_fm03.json")
DATA_FM03 = _load_json("data_fm03.json")
METADATA_FF = _load_json("metadata_ff.json")
DATA_FF = _load_json("data_ff.json")
METADATA_OB01 = _load_json("metadata_ob01.json")
DATA_OB01 = _load_json("data_ob01.json")
METADATA_PF01 = _load_json("metadata_pf01.json")
DATA_PF01 = _load_json("data_pf01.json")
METADATA_BIS = _load_json("metadata_bis.json")
DATA_BIS = _load_json("data_bis.json")


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
        assert frequency_matches("ANNUAL", Frequency.CY) is True

    def test_annual_cy_variant(self):
        assert frequency_matches("ANNUAL(MAR)", Frequency.CY) is True

    def test_annual_fy(self):
        assert frequency_matches("ANNUAL(MAR)", Frequency.FY) is True

    def test_annual_fy_no_match_plain(self):
        assert frequency_matches("ANNUAL", Frequency.FY) is False

    def test_mismatch(self):
        assert frequency_matches("DAILY", Frequency.M) is False

    def test_none(self):
        assert frequency_matches(None, Frequency.D) is False

    def test_semiannual_cy(self):
        assert frequency_matches("SEMIANNUAL", Frequency.CH) is True

    def test_semiannual_cy_variant(self):
        assert frequency_matches("SEMIANNUAL(SEP)", Frequency.CH) is True

    def test_semiannual_fy(self):
        assert frequency_matches("SEMIANNUAL(SEP)", Frequency.FH) is True

    def test_semiannual_fy_no_match_plain(self):
        assert frequency_matches("SEMIANNUAL", Frequency.FH) is False


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


class TestFinancialMarkets:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "FM03", METADATA_FM03)
        _mock_data(respx, "FM03", DATA_FM03)
        boj = BOJ()
        results = boj.financial_markets(db=Database.SHORT_TERM_MONEY_OUTSTANDING)
        assert len(results) == 1
        assert isinstance(results[0], FinancialMarket)
        boj.close()


class TestBalanceSheets:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "BS01", METADATA_BS01)
        _mock_data(respx, "BS01", DATA_BS01)
        boj = BOJ()
        results = boj.balance_sheets()
        assert len(results) == 1
        assert isinstance(results[0], BalanceSheet)
        assert results[0].institution_type == InstitutionType.BOJ
        boj.close()


class TestFlowOfFunds:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "FF", METADATA_FF)
        _mock_data(respx, "FF", DATA_FF)
        boj = BOJ()
        results = boj.flow_of_funds()
        assert len(results) == 1
        assert isinstance(results[0], FlowOfFunds)
        boj.close()


class TestBOJOperations:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "OB01", METADATA_OB01)
        _mock_data(respx, "OB01", DATA_OB01)
        boj = BOJ()
        results = boj.boj_operations()
        assert len(results) == 1
        assert isinstance(results[0], BOJOperation)
        boj.close()


class TestPublicFinance:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "PF01", METADATA_PF01)
        _mock_data(respx, "PF01", DATA_PF01)
        boj = BOJ()
        results = boj.public_finance()
        assert len(results) == 1
        assert isinstance(results[0], PublicFinance)
        boj.close()


class TestInternational:
    @respx.mock
    def test_basic(self):
        _mock_metadata(respx, "BIS", METADATA_BIS)
        _mock_data(respx, "BIS", DATA_BIS)
        boj = BOJ()
        results = boj.international()
        assert len(results) == 1
        assert isinstance(results[0], InternationalStat)
        boj.close()
