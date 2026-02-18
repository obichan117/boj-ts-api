# Getting Started

## Installation

```bash
pip install boj-ts-api
```

## Basic Usage

### Fetch Data by Series Code

```python
from boj_ts_api import BOJClient

with BOJClient(lang="en") as client:
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
with BOJClient(lang="en") as client:
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "data points")
```

### Fetch Data by Layer

```python
with BOJClient(lang="en") as client:
    resp = client.get_data_layer(db="FM08", frequency="D", layer="1,1")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES[:5])
```

### Metadata

```python
with BOJClient(lang="en") as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET:
        print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)
```

### CSV and pandas

```python
from boj_ts_api import BOJClient, csv_to_dataframe

with BOJClient(lang="en") as client:
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
from boj_ts_api import AsyncBOJClient

async def main():
    async with AsyncBOJClient(lang="en") as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].SERIES_CODE)

asyncio.run(main())
```

## CLI

Install the CLI extra:

```bash
pip install boj-ts-api[cli]
```

```bash
# Fetch data by code
bojts get-data-code --db CO --code TK99F1000601GCQ01000

# Fetch metadata
bojts get-metadata --db FM08

# CSV output
bojts get-data-code --db CO --code TK99F1000601GCQ01000 --format csv

# Japanese language
bojts --lang jp get-metadata --db FM08
```
