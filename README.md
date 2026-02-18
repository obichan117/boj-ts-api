# pyboj

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/pyboj)](https://pypi.org/project/pyboj/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Sync & async** clients with identical API surface (`Client` / `AsyncClient`)
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV support** with optional pandas DataFrame conversion
- **PEP 561** typed package

## Installation

```bash
pip install pyboj
```

Optional extras:

```bash
pip install pyboj[pandas]   # pandas DataFrame support
```

## Quick Start

```python
from pyboj._api import Client

with Client(lang="en") as client:
    # Fetch CPI data for Tokyo
    resp = client.get_data_code(
        db="CO",
        code="TK99F1000601GCQ01000",
        start_date="202401",
        end_date="202404",
    )
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES)

    # Auto-paginate all results
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "periods")

    # Metadata
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:3]:
        print(rec.SERIES_CODE, rec.NAME_OF_TIME_SERIES)
```

### Async

```python
import asyncio
from pyboj._api import AsyncClient

async def main():
    async with AsyncClient(lang="en") as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].VALUES.VALUES)

asyncio.run(main())
```

### CSV + pandas

```python
from pyboj._api import Client
from pyboj import csv_to_dataframe

with Client(lang="en") as client:
    csv_text = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")
    df = csv_to_dataframe(csv_text)
    print(df.head())
```

## API Endpoints

| Method | Endpoint | Client Method |
|--------|----------|---------------|
| Code API | `/api/v1/getDataCode` | `get_data_code()`, `iter_data_code()`, `get_data_code_csv()` |
| Layer API | `/api/v1/getDataLayer` | `get_data_layer()`, `iter_data_layer()`, `get_data_layer_csv()` |
| Metadata API | `/api/v1/getMetadata` | `get_metadata()`, `get_metadata_csv()` |

## License

MIT
