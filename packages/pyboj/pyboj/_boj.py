"""High-level BOJ client with typed domain methods."""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from boj_ts_api import Client, Frequency, Lang, MetadataRecord, MetadataResponse
from boj_ts_api._types.config import MAX_SERIES_PER_REQUEST

from pyboj._config import Database
from pyboj._domains._base import Series
from pyboj._domains.balance_of_payments import BalanceOfPayments, BopAccount
from pyboj._domains.exchange_rate import (
    Currency,
    ExchangeRate,
    RateType,
    _detect_currency,
    _detect_rate_type,
)
from pyboj._domains.interest_rate import (
    Collateralization,
    InterestRate,
    RateCategory,
    _detect_collateralization,
    _detect_rate_category,
)
from pyboj._domains.loan import IndustrySector, Loan
from pyboj._domains.money_deposit import Adjustment, MonetaryComponent, MoneyDeposit
from pyboj._domains.price_index import IndexType, PriceIndex, _detect_index_type
from pyboj._domains.tankan import (
    Tankan,
    TankanIndustry,
    TankanItem,
    TankanSeriesType,
    TankanSize,
    TankanTiming,
)
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

    def __init__(self, lang: Lang = Lang.EN, timeout: float = 30.0) -> None:
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
        # Batch codes in groups of MAX_SERIES_PER_REQUEST (250)
        for i in range(0, len(codes), MAX_SERIES_PER_REQUEST):
            batch = codes[i : i + MAX_SERIES_PER_REQUEST]
            code_str = ",".join(batch)
            for sr in self._client.iter_data_code(
                db=db_str, code=code_str, start_date=start_date, end_date=end_date
            ):
                results.append(wrapper(sr))
        return results

    def _simple_fetch(
        self,
        db: str | Database,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Series]:
        """Fetch all series from a database, optionally filtered by frequency."""
        return self._filter_and_fetch(
            db,
            lambda _rec: True,
            Series,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
        )

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

    # ── Light wrappers (return list[Series]) ─────────────────────────

    def financial_markets(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.SHORT_TERM_MONEY_OUTSTANDING,
    ) -> list[Series]:
        """Fetch financial markets series (FM03-FM07).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: FM03.
        """
        return self._simple_fetch(
            db, frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def balance_sheets(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.BOJ_ACCOUNTS,
    ) -> list[Series]:
        """Fetch balance sheet series (BS01-BS02).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: BS01.
        """
        return self._simple_fetch(
            db, frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def flow_of_funds(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Series]:
        """Fetch flow of funds series (FF).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        """
        return self._simple_fetch(
            Database.FLOW_OF_FUNDS, frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def boj_operations(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.GOVT_TRANSACTIONS,
    ) -> list[Series]:
        """Fetch BOJ operations series (OB01-OB02).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: OB01.
        """
        return self._simple_fetch(
            db, frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def public_finance(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.TREASURY_RECEIPTS_PAYMENTS,
    ) -> list[Series]:
        """Fetch public finance series (PF01-PF02).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: PF01.
        """
        return self._simple_fetch(
            db, frequency=frequency, start_date=start_date, end_date=end_date,
        )

    def international(
        self,
        *,
        frequency: Frequency | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        db: Database = Database.BIS_BANKING_STATISTICS,
    ) -> list[Series]:
        """Fetch international statistics series (BIS, DER, PS01, PS02, OT).

        Parameters
        ----------
        frequency:
            Filter by frequency.
        start_date:
            Start date in ``YYYYMM`` format.
        end_date:
            End date in ``YYYYMM`` format.
        db:
            Database to query. Default: BIS.
        """
        return self._simple_fetch(
            db, frequency=frequency, start_date=start_date, end_date=end_date,
        )
