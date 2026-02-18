"""Configuration constants for pyboj."""

from __future__ import annotations

from enum import Enum


class Database(str, Enum):
    """BOJ Time-Series Statistics database codes.

    Each member maps to a database identifier used by the BOJ API.
    Because ``Database`` inherits from ``str``, members can be passed
    directly to :pymeth:`Client.get_data_code` as the ``db`` argument.
    """

    # ── Interest Rates on Deposits and Loans ─────────────────────────
    BASIC_DISCOUNT_RATE = "IR01"
    DEPOSIT_RATES_POSTED = "IR02"
    TIME_DEPOSIT_RATES = "IR03"
    LOAN_RATES = "IR04"

    # ── Financial Markets ─────────────────────────────────────────────
    CALL_RATES = "FM01"
    MONEY_MARKET_RATES = "FM02"
    SHORT_TERM_MONEY_OUTSTANDING = "FM03"
    CALL_MONEY_OUTSTANDING = "FM04"
    PUBLIC_CORPORATE_BONDS = "FM05"
    GOVT_BOND_TRADING = "FM06"
    GOVT_BOND_OTC_SALES = "FM07"
    EXCHANGE_RATES = "FM08"
    EFFECTIVE_EXCHANGE_RATES = "FM09"

    # ── Money and Deposits ────────────────────────────────────────────
    MONETARY_BASE = "MD01"
    MONEY_STOCK = "MD02"
    MONETARY_SURVEY = "MD03"
    MONEY_STOCK_CHANGES = "MD04"
    CURRENCY_IN_CIRCULATION = "MD05"
    CURRENT_ACCOUNT_CHANGES = "MD06"
    RESERVES = "MD07"
    CURRENT_ACCOUNT_BY_SECTOR = "MD08"
    MONETARY_BASE_TRANSACTIONS = "MD09"
    DEPOSITS_BY_DEPOSITOR = "MD10"
    DEPOSITS_VAULT_CASH_LOANS = "MD11"
    DEPOSITS_BY_PREFECTURE = "MD12"
    FINANCIAL_INSTITUTIONS_FIGURES = "MD13"
    TIME_DEPOSITS_BY_MATURITY = "MD14"

    # ── Loans ─────────────────────────────────────────────────────────
    LOANS_BY_SECTOR = "LA01"
    BOJ_LOANS = "LA02"
    LOANS_OTHER = "LA03"
    COMMITMENT_LINES = "LA04"
    LOAN_OFFICER_SURVEY = "LA05"

    # ── Balance Sheets ────────────────────────────────────────────────
    BOJ_ACCOUNTS = "BS01"
    FINANCIAL_INSTITUTIONS_ACCOUNTS = "BS02"

    # ── Flow of Funds ─────────────────────────────────────────────────
    FLOW_OF_FUNDS = "FF"

    # ── BOJ Operations ────────────────────────────────────────────────
    GOVT_TRANSACTIONS = "OB01"
    BOJ_COLLATERAL = "OB02"

    # ── TANKAN ────────────────────────────────────────────────────────
    TANKAN = "CO"

    # ── Prices ────────────────────────────────────────────────────────
    PRODUCER_PRICE_INDEX = "PR01"
    SERVICES_PRICE_INDEX = "PR02"
    INPUT_OUTPUT_PRICE_INDEX = "PR03"
    FINAL_DEMAND_PRICE_INDEX = "PR04"

    # ── Public Finance ────────────────────────────────────────────────
    TREASURY_RECEIPTS_PAYMENTS = "PF01"
    NATIONAL_GOVT_DEBT = "PF02"

    # ── Balance of Payments ───────────────────────────────────────────
    BALANCE_OF_PAYMENTS = "BP01"

    # ── International / Other ─────────────────────────────────────────
    BIS_BANKING_STATISTICS = "BIS"
    DERIVATIVES_MARKET = "DER"
    PAYMENT_SETTLEMENT_SYSTEMS = "PS01"
    SETTLEMENT_FAILS = "PS02"
    OTHER = "OT"
