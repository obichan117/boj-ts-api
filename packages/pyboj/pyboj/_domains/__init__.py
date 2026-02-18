"""Domain wrapper objects for BOJ time-series data."""

from pyboj._domains._base import Series
from pyboj._domains.balance_of_payments import BalanceOfPayments, BopAccount
from pyboj._domains.exchange_rate import Currency, ExchangeRate, RateType
from pyboj._domains.interest_rate import (
    Collateralization,
    InterestRate,
    RateCategory,
)
from pyboj._domains.loan import IndustrySector, Loan
from pyboj._domains.money_deposit import Adjustment, MonetaryComponent, MoneyDeposit
from pyboj._domains.price_index import IndexType, PriceIndex
from pyboj._domains.tankan import (
    Tankan,
    TankanIndustry,
    TankanItem,
    TankanSeriesType,
    TankanSize,
    TankanTiming,
)

__all__ = [
    "Adjustment",
    "BalanceOfPayments",
    "BopAccount",
    "Collateralization",
    "Currency",
    "ExchangeRate",
    "IndexType",
    "IndustrySector",
    "InterestRate",
    "Loan",
    "MonetaryComponent",
    "MoneyDeposit",
    "PriceIndex",
    "RateCategory",
    "RateType",
    "Series",
    "Tankan",
    "TankanIndustry",
    "TankanItem",
    "TankanSeriesType",
    "TankanSize",
    "TankanTiming",
]
