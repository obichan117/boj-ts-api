"""High-level BOJ client with typed domain methods."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from boj_ts_api import Client, Frequency, Lang, MetadataRecord, MetadataResponse
from boj_ts_api._types.config import DEFAULT_TIMEOUT

from pyboj._config import Database
from pyboj._domains._base import Series
from pyboj._domains.balance_of_payments import BalanceOfPayments, BopAccount
from pyboj._domains.balance_sheet import (
    AccountSide,
    BalanceSheet,
    InstitutionType,
    _detect_institution,
    _detect_side,
)
from pyboj._domains.boj_operation import BOJOperation, OperationType, _detect_operation
from pyboj._domains.exchange_rate import (
    Currency,
    ExchangeRate,
    RateType,
    _detect_currency,
    _detect_rate_type,
)
from pyboj._domains.financial_market import (
    FinancialMarket,
    InstrumentType,
    MarketSegment,
    _detect_instrument,
    _detect_segment,
)
from pyboj._domains.flow_of_funds import (
    FlowOfFunds,
    FofInstrument,
    FofSector,
    _detect_fof_instrument,
    _detect_fof_sector,
)
from pyboj._domains.interest_rate import (
    Collateralization,
    InterestRate,
    RateCategory,
    _detect_collateralization,
    _detect_rate_category,
)
from pyboj._domains.international_stat import (
    InternationalStat,
    StatCategory,
    _detect_stat_category,
)
from pyboj._domains.loan import IndustrySector, Loan
from pyboj._domains.money_deposit import Adjustment, MonetaryComponent, MoneyDeposit
from pyboj._domains.price_index import IndexType, PriceIndex, _detect_index_type
from pyboj._domains.public_finance import FiscalItem, PublicFinance, _detect_fiscal_item
from pyboj._domains.tankan import (
    Tankan,
    TankanIndustry,
    TankanItem,
    TankanSeriesType,
    TankanSize,
    TankanTiming,
)
from pyboj._helpers.layer_tree import LayerNode, build_layer_tree, search_metadata
from pyboj._utils import frequency_matches

_T = TypeVar("_T", bound=Series)


class BOJ:
    """High-level client for the Bank of Japan Time-Series Statistics API.

    Every parameter is typed — no magic strings. The client fetches metadata,
    filters series by your criteria, and returns rich domain wrapper objects.

    Usage::

        from pyboj import BOJ, Currency, Frequency

        boj = BOJ()
        rates = boj.exchange_rates(currency=Currency.USD_JPY, frequency=Frequency.D)
        for r in rates:
            print(r.currency_pair, r.values[:3])
            df = r.to_dataframe()

    Or as a context manager::

        with BOJ() as boj:
            rates = boj.exchange_rates(currency=Currency.USD_JPY)
    """

    def __init__(self, lang: Lang = Lang.EN, timeout: float = DEFAULT_TIMEOUT) -> None:
        self._client = Client(lang=lang, timeout=timeout)
        self._metadata_cache: dict[str, MetadataResponse] = {}

    def __enter__(self) -> BOJ:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    # ── Metadata ─────────────────────────────────────────────────────

    def _get_metadata(self, db: str | Database) -> MetadataResponse:
        """Fetch metadata, using a per-database cache."""
        key = db.value if isinstance(db, Database) else db
        if key not in self._metadata_cache:
            self._metadata_cache[key] = self._client.get_metadata(db=key)
        return self._metadata_cache[key]

    def metadata(self, db: Database) -> list[MetadataRecord]:
        """Return metadata records for a database.

        Parameters
        ----------
        db:
            Database to query.
        """
        return self._get_metadata(db).RESULTSET

    # ── Core fetch logic ─────────────────────────────────────────────

    def _filter_and_fetch(
        self,
        db: str | Database,
        predicate: Callable[[MetadataRecord], bool],
        wrapper: type[_T],
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[_T]:
        """Fetch series matching a metadata predicate.

        1. Get metadata for the database (cached).
        2. Skip header rows (empty SERIES_CODE).
        3. Filter by frequency if requested.
        4. Apply the domain-specific predicate.
        5. Batch matching codes (max 250 per request).
        6. Fetch via iter_data_code and wrap results.
        """
        meta = self._get_metadata(db)
        codes: list[str] = []
        for rec in meta.RESULTSET:
            if not rec.SERIES_CODE:
                continue
            if frequency is not None and not frequency_matches(rec.FREQUENCY, frequency):
                continue
            if not predicate(rec):
                continue
            codes.append(rec.SERIES_CODE)

        if not codes:
            return []

        db_str = db.value if isinstance(db, Database) else db
        results: list[_T] = []
        # Batch codes so that the comma-separated string stays under the URL
        # length limit of the BOJ API.  We cap the code parameter at 1000
        # characters to leave room for the rest of the URL (path, other params).
        max_code_len = 1000
        batches: list[list[str]] = [[]]
        cur_len = 0
        for code in codes:
            added_len = len(code) + (1 if batches[-1] else 0)  # comma separator
            if batches[-1] and cur_len + added_len > max_code_len:
                batches.append([])
                cur_len = 0
            batches[-1].append(code)
            cur_len += added_len

        for batch in batches:
            code_str = ",".join(batch)
            for sr in self._client.iter_data_code(
                db=db_str, code=code_str, start_date=start_date, end_date=end_date
            ):
                results.append(wrapper(sr))
        return results

    # ── Domain methods ───────────────────────────────────────────────

    def exchange_rates(
        self,
        *,
        currency: Currency | None = None,
        rate_type: RateType | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.EXCHANGE_RATES,
    ) -> list[ExchangeRate]:
        """Fetch exchange rate series.

        Parameters
        ----------
        currency:
            Filter by currency pair (e.g. ``Currency.USD_JPY``).
        rate_type:
            Filter by rate type (e.g. ``RateType.SPOT_9AM``).
        frequency:
            Filter by frequency (e.g. ``Frequency.D``).
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: FM08 (Exchange Rates).
        """

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if currency is not None and _detect_currency(name) != currency:
                return False
            return rate_type is None or _detect_rate_type(name) == rate_type

        return self._filter_and_fetch(
            db, predicate, ExchangeRate,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def interest_rates(
        self,
        *,
        category: RateCategory | None = None,
        collateralization: Collateralization | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.CALL_RATES,
    ) -> list[InterestRate]:
        """Fetch interest rate series.

        Parameters
        ----------
        category:
            Filter by rate category (e.g. ``RateCategory.CALL_RATE``).
        collateralization:
            Filter by collateralization type.
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: FM01 (Call Rates).
        """

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if category is not None and _detect_rate_category(name) != category:
                return False
            return (
                collateralization is None
                or _detect_collateralization(name) == collateralization
            )

        return self._filter_and_fetch(
            db, predicate, InterestRate,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def price_indices(
        self,
        *,
        index_type: IndexType | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.PRODUCER_PRICE_INDEX,
    ) -> list[PriceIndex]:
        """Fetch price index series.

        Parameters
        ----------
        index_type:
            Filter by index type (e.g. ``IndexType.PRODUCER``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: PR01 (Producer Price Index).
        """

        def predicate(rec: MetadataRecord) -> bool:
            if index_type is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                cat = rec.CATEGORY or ""
                if _detect_index_type(name, cat) != index_type:
                    return False
            return True

        return self._filter_and_fetch(
            db, predicate, PriceIndex,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def tankan(
        self,
        *,
        industry: TankanIndustry | None = None,
        size: TankanSize | None = None,
        item: TankanItem | None = None,
        series_type: TankanSeriesType | None = None,
        timing: TankanTiming | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Tankan]:
        """Fetch TANKAN survey series.

        Parameters
        ----------
        industry:
            Filter by industry classification.
        size:
            Filter by enterprise size.
        item:
            Filter by survey item.
        series_type:
            Filter by series type (DI, percent point, etc.).
        timing:
            Filter by timing (actual vs forecast).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        """
        from pyboj._domains.tankan import _matches_tankan_filters

        def predicate(rec: MetadataRecord) -> bool:
            return _matches_tankan_filters(
                rec, industry=industry, size=size, item=item,
                series_type=series_type, timing=timing,
            )

        return self._filter_and_fetch(
            Database.TANKAN, predicate, Tankan,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def balance_of_payments(
        self,
        *,
        account: BopAccount | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[BalanceOfPayments]:
        """Fetch balance of payments series.

        Parameters
        ----------
        account:
            Filter by BOP account type.
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        """
        from pyboj._domains.balance_of_payments import _detect_bop_account

        def predicate(rec: MetadataRecord) -> bool:
            if account is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                if _detect_bop_account(name) != account:
                    return False
            return True

        return self._filter_and_fetch(
            Database.BALANCE_OF_PAYMENTS, predicate, BalanceOfPayments,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def money_deposits(
        self,
        *,
        component: MonetaryComponent | None = None,
        adjustment: Adjustment | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.MONETARY_BASE,
    ) -> list[MoneyDeposit]:
        """Fetch money and deposit series.

        Parameters
        ----------
        component:
            Filter by monetary component.
        adjustment:
            Filter by adjustment type.
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: MD01 (Monetary Base).
        """
        from pyboj._domains.money_deposit import _detect_adjustment, _detect_component

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if component is not None and _detect_component(name) != component:
                return False
            return adjustment is None or _detect_adjustment(name) == adjustment

        return self._filter_and_fetch(
            db, predicate, MoneyDeposit,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def loans(
        self,
        *,
        sector: IndustrySector | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.LOANS_BY_SECTOR,
    ) -> list[Loan]:
        """Fetch loan series.

        Parameters
        ----------
        sector:
            Filter by industry sector.
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: LA01 (Loans by Sector).
        """
        from pyboj._domains.loan import _detect_sector

        def predicate(rec: MetadataRecord) -> bool:
            if sector is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                if _detect_sector(name) != sector:
                    return False
            return True

        return self._filter_and_fetch(
            db, predicate, Loan,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    # ── Rich wrappers (formerly light wrappers) ──────────────────────

    def financial_markets(
        self,
        *,
        segment: MarketSegment | None = None,
        instrument_type: InstrumentType | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.SHORT_TERM_MONEY_OUTSTANDING,
    ) -> list[FinancialMarket]:
        """Fetch financial markets series (FM03-FM07).

        Parameters
        ----------
        segment:
            Filter by market segment (e.g. ``MarketSegment.GOVT_BONDS``).
        instrument_type:
            Filter by instrument type (e.g. ``InstrumentType.OUTSTANDING``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: FM03.
        """

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if segment is not None and _detect_segment(name) != segment:
                return False
            return instrument_type is None or _detect_instrument(name) == instrument_type

        return self._filter_and_fetch(
            db, predicate, FinancialMarket,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def balance_sheets(
        self,
        *,
        account_side: AccountSide | None = None,
        institution_type: InstitutionType | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.BOJ_ACCOUNTS,
    ) -> list[BalanceSheet]:
        """Fetch balance sheet series (BS01-BS02).

        Parameters
        ----------
        account_side:
            Filter by balance sheet side (e.g. ``AccountSide.ASSETS``).
        institution_type:
            Filter by institution type (e.g. ``InstitutionType.BOJ``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: BS01.
        """

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if account_side is not None and _detect_side(name) != account_side:
                return False
            return institution_type is None or _detect_institution(name) == institution_type

        return self._filter_and_fetch(
            db, predicate, BalanceSheet,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def flow_of_funds(
        self,
        *,
        sector: FofSector | None = None,
        instrument: FofInstrument | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[FlowOfFunds]:
        """Fetch flow of funds series (FF).

        Parameters
        ----------
        sector:
            Filter by economic sector (e.g. ``FofSector.HOUSEHOLDS``).
        instrument:
            Filter by financial instrument (e.g. ``FofInstrument.EQUITY``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        """

        def predicate(rec: MetadataRecord) -> bool:
            name = rec.NAME_OF_TIME_SERIES or ""
            if sector is not None and _detect_fof_sector(name) != sector:
                return False
            return instrument is None or _detect_fof_instrument(name) == instrument

        return self._filter_and_fetch(
            Database.FLOW_OF_FUNDS, predicate, FlowOfFunds,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def boj_operations(
        self,
        *,
        operation_type: OperationType | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.GOVT_TRANSACTIONS,
    ) -> list[BOJOperation]:
        """Fetch BOJ operations series (OB01-OB02).

        Parameters
        ----------
        operation_type:
            Filter by operation type (e.g. ``OperationType.JGB_OPERATIONS``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: OB01.
        """

        def predicate(rec: MetadataRecord) -> bool:
            if operation_type is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                if _detect_operation(name) != operation_type:
                    return False
            return True

        return self._filter_and_fetch(
            db, predicate, BOJOperation,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def public_finance(
        self,
        *,
        fiscal_item: FiscalItem | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.TREASURY_RECEIPTS_PAYMENTS,
    ) -> list[PublicFinance]:
        """Fetch public finance series (PF01-PF02).

        Parameters
        ----------
        fiscal_item:
            Filter by fiscal item (e.g. ``FiscalItem.TAX_REVENUE``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: PF01.
        """

        def predicate(rec: MetadataRecord) -> bool:
            if fiscal_item is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                if _detect_fiscal_item(name) != fiscal_item:
                    return False
            return True

        return self._filter_and_fetch(
            db, predicate, PublicFinance,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def international(
        self,
        *,
        stat_category: StatCategory | None = None,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.BIS_BANKING_STATISTICS,
    ) -> list[InternationalStat]:
        """Fetch international statistics series (BIS, DER, PS01, PS02, OT).

        Parameters
        ----------
        stat_category:
            Filter by statistics category (e.g. ``StatCategory.DERIVATIVES``).
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: BIS.
        """

        def predicate(rec: MetadataRecord) -> bool:
            if stat_category is not None:
                name = rec.NAME_OF_TIME_SERIES or ""
                if _detect_stat_category(name) != stat_category:
                    return False
            return True

        return self._filter_and_fetch(
            db, predicate, InternationalStat,
            frequency=frequency, start_date=start_date, end_date=end_date,
        )

    # ── Discovery ────────────────────────────────────────────────────

    def layer_tree(self, db: Database) -> LayerNode:
        """Build a hierarchical layer tree from database metadata.

        Parameters
        ----------
        db:
            Database to build the tree for.

        Returns
        -------
        LayerNode
            Root node of the layer hierarchy.
        """
        records = self.metadata(db)
        return build_layer_tree(records)

    def search(self, db: Database, query: str) -> list[MetadataRecord]:
        """Search metadata records by keyword.

        Parameters
        ----------
        db:
            Database to search.
        query:
            Case-insensitive search string.

        Returns
        -------
        list[MetadataRecord]
            Matching metadata records.
        """
        records = self.metadata(db)
        return search_metadata(records, query)
