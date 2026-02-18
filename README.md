# pyboj

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/pyboj)](https://pypi.org/project/pyboj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Wraps the official BOJ API ([announced 2026-02-18](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)) for machine-readable access to Japan's central bank time-series data.

## Installation

```bash
pip install pyboj[pandas]   # recommended — includes DataFrame support
pip install pyboj            # without pandas
pip install boj-ts-api       # low-level client only
```

## Quick Start

```python
from pyboj import BOJ, Currency, Frequency

boj = BOJ()

# Fetch USD/JPY daily exchange rates for Jan-Mar 2024
rates = boj.exchange_rates(
    currency=Currency.USD_JPY,
    frequency=Frequency.D,
    start_date="202401",
    end_date="202403",
)

for r in rates:
    print(r.currency_pair, r.rate_type)
    print(r.dates[:3])    # [datetime.date(2024, 1, 4), ...]
    print(r.values[:3])   # [144.62, 145.30, ...]

# Convert to pandas DataFrame
df = rates[0].to_dataframe()
df.plot(title="USD/JPY", figsize=(10, 4))
```

### More Examples

```python
from pyboj import (
    BOJ, Currency, Frequency, Database,
    RateCategory, TankanIndustry, TankanSize,
    IndexType, BopAccount, MonetaryComponent, IndustrySector,
)

boj = BOJ()

# Interest rates — filter by category
rates = boj.interest_rates(
    category=RateCategory.CALL_RATE,
    frequency=Frequency.D,
    start_date="202401",
)
for r in rates:
    print(r.rate_category, r.collateralization, r.tenor)
    #  RateCategory.CALL_RATE  Collateralization.UNCOLLATERALIZED  Overnight

# TANKAN survey — filter by industry and enterprise size
tankan = boj.tankan(
    industry=TankanIndustry.MANUFACTURING,
    size=TankanSize.LARGE,
    start_date="202301",
)
for t in tankan[:3]:
    print(t.industry, t.size, t.item, t.series_type)

# Price indices
indices = boj.price_indices(
    index_type=IndexType.PRODUCER,
    start_date="202401",
)
for idx in indices[:3]:
    print(idx.index_type, idx.base_year, idx.is_yoy_change)

# Balance of payments
bop = boj.balance_of_payments(account=BopAccount.CURRENT)

# Money & deposits — switch database with enum
money = boj.money_deposits(
    component=MonetaryComponent.M2,
    db=Database.MONEY_STOCK,
)

# Loans by sector
loans = boj.loans(sector=IndustrySector.MANUFACTURING)

# Metadata — inspect available series before fetching
records = boj.metadata(Database.EXCHANGE_RATES)
for rec in records[:5]:
    print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)

boj.close()
```

### Context Manager

```python
with BOJ() as boj:
    rates = boj.exchange_rates(currency=Currency.USD_JPY)
    # client auto-closes on exit
```

## API Overview

### `BOJ` Client Methods

Every method returns typed domain objects with parsed dates, numeric values, and `to_dataframe()`.

| Method | Returns | Filter Enums | Default DB |
|--------|---------|-------------|------------|
| `exchange_rates()` | `list[ExchangeRate]` | `Currency`, `RateType` | FM08 |
| `interest_rates()` | `list[InterestRate]` | `RateCategory`, `Collateralization` | FM01 |
| `price_indices()` | `list[PriceIndex]` | `IndexType` | PR01 |
| `tankan()` | `list[Tankan]` | `TankanIndustry`, `TankanSize`, `TankanItem`, `TankanSeriesType`, `TankanTiming` | CO |
| `balance_of_payments()` | `list[BalanceOfPayments]` | `BopAccount` | BP01 |
| `money_deposits()` | `list[MoneyDeposit]` | `MonetaryComponent`, `Adjustment` | MD01 |
| `loans()` | `list[Loan]` | `IndustrySector` | LA01 |
| `financial_markets()` | `list[Series]` | — | FM03 |
| `balance_sheets()` | `list[Series]` | — | BS01 |
| `flow_of_funds()` | `list[Series]` | — | FF |
| `boj_operations()` | `list[Series]` | — | OB01 |
| `public_finance()` | `list[Series]` | — | PF01 |
| `international()` | `list[Series]` | — | BIS |
| `metadata()` | `list[MetadataRecord]` | — | — |

All methods accept `frequency`, `start_date`, `end_date`. Methods with a default DB accept a `db` parameter to query other databases (e.g. `db=Database.MONEY_STOCK`).

### Domain Wrapper Properties

Every domain object inherits from `Series`:

| Property | Type | Description |
|----------|------|-------------|
| `series_code` | `str` | BOJ series code |
| `name` / `name_jp` | `str \| None` | English / Japanese series name |
| `unit` / `unit_jp` | `str \| None` | Unit label |
| `frequency` | `str \| None` | Frequency string (e.g. `"DAILY"`) |
| `dates` | `list[datetime.date]` | Parsed survey dates |
| `values` | `list[float \| None]` | Numeric values |
| `to_dataframe()` | `DataFrame` | pandas DataFrame with DatetimeIndex |

Subclasses add domain-specific properties (e.g. `ExchangeRate.currency_pair`, `InterestRate.tenor`, `PriceIndex.base_year`).

### `Database` Enum (43 databases)

Named constants for all BOJ database codes — use instead of magic strings:

| Category | Databases |
|----------|-----------|
| Interest Rates | `IR01`–`IR04` |
| Financial Markets | `FM01`–`FM09` |
| Money & Deposits | `MD01`–`MD14` |
| Loans | `LA01`–`LA05` |
| Balance Sheets | `BS01`–`BS02` |
| Flow of Funds | `FF` |
| BOJ Operations | `OB01`–`OB02` |
| TANKAN | `CO` |
| Prices | `PR01`–`PR04` |
| Public Finance | `PF01`–`PF02` |
| Balance of Payments | `BP01` |
| International | `BIS`, `DER`, `PS01`, `PS02`, `OT` |

## Features

- **`BOJ` client** — typed domain methods for all 13 BOJ categories (43 databases)
- **Enum-driven filtering** — `Currency`, `RateType`, `TankanIndustry`, `BopAccount`, etc.
- **Domain wrappers** — `ExchangeRate`, `InterestRate`, `PriceIndex`, `Tankan`, and more
- **Metadata-driven** — auto-fetches metadata and filters series by your criteria
- **Sync & async** low-level clients with identical API surface
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV + pandas** support with `to_dataframe()` and `csv_to_dataframe()`
- **PEP 561** typed package

## Packages

| Package | Install | Description |
|---------|---------|-------------|
| **pyboj** | `pip install pyboj` | High-level client with domain wrappers and pandas support |
| **boj-ts-api** | `pip install boj-ts-api` | Low-level typed API client |

## Advanced: Low-Level API

```python
from boj_ts_api import Client, Lang

with Client(lang=Lang.EN) as client:
    # Fetch data by series code
    resp = client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)

    # Auto-paginate
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "periods")

    # Metadata
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:3]:
        print(rec.SERIES_CODE, rec.NAME_OF_TIME_SERIES)
```

## Documentation

- [Getting Started](https://obichan117.github.io/pyboj/getting-started/)
- [API Reference](https://obichan117.github.io/pyboj/api-reference/)
- [Upstream BOJ API Reference](https://obichan117.github.io/pyboj/boj-api/)
- [OpenAPI Specification (Interactive)](https://obichan117.github.io/pyboj/openapi-spec/)

## Official BOJ Resources

- [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
- [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)

## License

MIT
