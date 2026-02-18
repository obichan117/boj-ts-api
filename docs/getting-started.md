# Getting Started

## Installation

```bash
pip install boj-ts-api
```

Or for the beginner-friendly wrapper with optional pandas support:

```bash
pip install pyboj[pandas]
```

## Basic Usage

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

For large result sets, use the iterator methods to automatically follow pagination:

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

### Metadata

```python
with Client(lang=Lang.EN) as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET:
        print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)
```

### CSV and pandas

```python
from pyboj import Client, Lang, csv_to_dataframe

with Client(lang=Lang.EN) as client:
    csv_text = client.get_data_code_csv(
        db="CO", code="TK99F1000601GCQ01000",
        start_date="202401", end_date="202404",
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

## Using the Database Enum

The `Database` enum provides named constants for all BOJ database codes, so you don't have to memorize raw strings like `"FM08"` or `"CO"`:

```python
from pyboj import Client, Lang, Database

with Client(lang=Lang.EN) as client:
    # Instead of db="FM08"
    resp = client.get_data_code(
        db=Database.EXCHANGE_RATES,
        code="FM08'MAINAVG",
    )

    # Instead of db="CO"
    meta = client.get_metadata(db=Database.TANKAN)
```

## Domain Wrappers

`pyboj` provides domain wrapper objects that add parsed dates, typed numeric values, and domain-specific properties on top of raw `SeriesResult` objects.

### ExchangeRate

Wraps exchange rate series from the FM08 / FM09 databases. Automatically detects the currency pair and rate type from the series name.

```python
from pyboj import Client, Lang, Database, ExchangeRate

with Client(lang=Lang.EN) as client:
    resp = client.get_data_code(
        db=Database.EXCHANGE_RATES,
        code="FM08'MAINAVG",
    )
    rate = ExchangeRate(resp.RESULTSET[0])

    print(rate.currency_pair)   # "USD/JPY"
    print(rate.rate_type)       # RateType.AVERAGE
    print(rate.dates[:3])       # [datetime.date(2024, 1, 1), ...]
    print(rate.values[:3])      # [148.12, 149.56, 151.34]

    # Convert to pandas DataFrame
    df = rate.to_dataframe()
    print(df.head())
```

### InterestRate

Wraps interest rate series from FM01, FM02, IR01-IR04. Detects rate category, collateralization type, and tenor.

```python
from pyboj import Client, Lang, Database, InterestRate

with Client(lang=Lang.EN) as client:
    resp = client.get_data_code(
        db=Database.CALL_RATES,
        code="FM01'MAINAVG",
    )
    rate = InterestRate(resp.RESULTSET[0])

    print(rate.rate_category)      # RateCategory.CALL_RATE
    print(rate.collateralization)   # Collateralization.UNCOLLATERALIZED
    print(rate.tenor)               # "Overnight"
```

### PriceIndex

Wraps price index series from PR01-PR04. Detects index type, base year, and whether the series is year-on-year change.

```python
from pyboj import Client, Lang, Database, PriceIndex

with Client(lang=Lang.EN) as client:
    resp = client.get_data_code(
        db=Database.PRODUCER_PRICE_INDEX,
        code="PR01'IALL_IALL000000000",
    )
    idx = PriceIndex(resp.RESULTSET[0])

    print(idx.index_type)    # IndexType.PRODUCER
    print(idx.base_year)     # "CY2020"
    print(idx.is_yoy_change) # False
```

## Finding Series Codes

To discover available series codes, use the [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/) or the metadata endpoint:

```python
with Client(lang=Lang.EN) as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:5]:
        print(f"{rec.SERIES_CODE}: {rec.NAME_OF_TIME_SERIES}")
```

See the [Upstream API Reference](boj-api.md) for details on all available parameters and database codes.
