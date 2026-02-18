# Getting Started

## Installation

```bash
pip install pyboj[pandas]
```

Or without pandas:

```bash
pip install pyboj
```

For direct low-level API access only:

```bash
pip install boj-ts-api
```

## High-Level API (Recommended)

The `BOJ` client provides typed domain methods for all 13 BOJ data categories. Every parameter is an enum — no magic strings.

### Exchange Rates

```python
from pyboj import BOJ, Currency, Frequency

boj = BOJ()

# Filter by currency pair and frequency
rates = boj.exchange_rates(
    currency=Currency.USD_JPY,
    frequency=Frequency.D,
    start_date="202401",
)
for r in rates:
    print(r.currency_pair)  # Currency.USD_JPY
    print(r.rate_type)      # RateType.SPOT_9AM
    print(r.values[:3])     # [141.75, 144.62, ...]
    df = r.to_dataframe()   # pandas DataFrame
```

### Interest Rates

```python
from pyboj import BOJ, RateCategory

boj = BOJ()
rates = boj.interest_rates(category=RateCategory.CALL_RATE)
for r in rates:
    print(r.rate_category)      # RateCategory.CALL_RATE
    print(r.collateralization)  # Collateralization.UNCOLLATERALIZED
    print(r.tenor)              # "Overnight"
```

### TANKAN Survey

```python
from pyboj import BOJ, TankanIndustry, TankanSize

boj = BOJ()
results = boj.tankan(
    industry=TankanIndustry.MANUFACTURING,
    size=TankanSize.LARGE,
)
for t in results:
    print(t.industry, t.size, t.item, t.series_type)
```

### Price Indices

```python
from pyboj import BOJ, IndexType

boj = BOJ()
indices = boj.price_indices(index_type=IndexType.PRODUCER)
for idx in indices:
    print(idx.index_type)    # IndexType.PRODUCER
    print(idx.base_year)     # "CY2020"
    print(idx.is_yoy_change) # False
```

### Balance of Payments

```python
from pyboj import BOJ, BopAccount

boj = BOJ()
results = boj.balance_of_payments(account=BopAccount.CURRENT)
```

### Money & Deposits

```python
from pyboj import BOJ, MonetaryComponent, Database

boj = BOJ()
results = boj.money_deposits(
    component=MonetaryComponent.TOTAL,
    db=Database.MONETARY_BASE,
)
```

### Loans

```python
from pyboj import BOJ, IndustrySector

boj = BOJ()
results = boj.loans(sector=IndustrySector.MANUFACTURING)
```

### Light Wrappers

These categories return generic `Series` objects with frequency filtering:

```python
boj = BOJ()

# Financial Markets (FM03-FM07)
series = boj.financial_markets(db=Database.SHORT_TERM_MONEY_OUTSTANDING)

# Balance Sheets (BS01-BS02)
series = boj.balance_sheets(db=Database.BOJ_ACCOUNTS)

# Flow of Funds
series = boj.flow_of_funds()

# BOJ Operations (OB01-OB02)
series = boj.boj_operations()

# Public Finance (PF01-PF02)
series = boj.public_finance()

# International (BIS, DER, PS01, PS02, OT)
series = boj.international()
```

### Using the Database Enum

The `Database` enum provides named constants for all 43 BOJ databases:

```python
from pyboj import Database

# Use with any method that accepts a db parameter
rates = boj.exchange_rates(db=Database.EFFECTIVE_EXCHANGE_RATES)
money = boj.money_deposits(db=Database.MONEY_STOCK)
loans = boj.loans(db=Database.COMMITMENT_LINES)
```

### Metadata

```python
from pyboj import BOJ, Database

boj = BOJ()
records = boj.metadata(Database.EXCHANGE_RATES)
for rec in records[:5]:
    print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)
```

## Advanced: Low-Level API

### Fetch Data by Series Code

```python
from boj_ts_api import Client, Lang

with Client(lang=Lang.EN) as client:
    resp = client.get_data_code(
        db="CO",
        code="TK99F1000601GCQ01000",
        start_date="202401",
        end_date="202404",
    )
    for series in resp.RESULTSET:
        print(f"{series.SERIES_CODE}: {series.VALUES.VALUES}")
```

### Auto-Pagination

```python
with Client(lang=Lang.EN) as client:
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "data points")
```

### Fetch Data by Layer

```python
from boj_ts_api import Frequency

with Client(lang=Lang.EN) as client:
    resp = client.get_data_layer(db="FM08", frequency=Frequency.D, layer="1,1")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES[:5])
```

### CSV and pandas

```python
from pyboj import Client, Lang, csv_to_dataframe

with Client(lang=Lang.EN) as client:
    csv_text = client.get_data_code_csv(
        db="CO", code="TK99F1000601GCQ01000",
    )
    df = csv_to_dataframe(csv_text)
    print(df.head())
```

### Async Client

```python
import asyncio
from boj_ts_api import AsyncClient, Lang

async def main():
    async with AsyncClient(lang=Lang.EN) as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].SERIES_CODE)

asyncio.run(main())
```

See the [Upstream API Reference](boj-api.md) for details on all available parameters and database codes.
