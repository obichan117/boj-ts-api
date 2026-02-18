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
from boj_ts_api import Client

with Client(lang="en") as client:
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
with Client(lang="en") as client:
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "data points")
```

### Fetch Data by Layer

```python
with Client(lang="en") as client:
    resp = client.get_data_layer(db="FM08", frequency="D", layer="1,1")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES[:5])
```

### Metadata

```python
with Client(lang="en") as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET:
        print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)
```

### CSV and pandas

```python
from pyboj import Client, csv_to_dataframe

with Client(lang="en") as client:
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
from boj_ts_api import AsyncClient

async def main():
    async with AsyncClient(lang="en") as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].SERIES_CODE)

asyncio.run(main())
```

## Finding Series Codes

To discover available series codes, use the [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/) or the metadata endpoint:

```python
with Client(lang="en") as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:5]:
        print(f"{rec.SERIES_CODE}: {rec.NAME_OF_TIME_SERIES}")
```

See the [Upstream API Reference](boj-api.md) for details on all available parameters and database codes.
