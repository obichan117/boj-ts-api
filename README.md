# boj-ts-api

Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/boj-ts-api)](https://pypi.org/project/boj-ts-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Features

- **Sync & async** clients with identical API surface (`BOJClient` / `AsyncBOJClient`)
- **Pydantic v2** models for type-safe, validated responses
- **Auto-pagination** via `iter_data_code()` / `iter_data_layer()` generators
- **CSV support** with optional pandas DataFrame conversion
- **CLI tool** (`bojts`) for quick terminal access
- **PEP 561** typed package

## Installation

```bash
pip install boj-ts-api
```

Optional extras:

```bash
pip install boj-ts-api[pandas]   # pandas DataFrame support
pip install boj-ts-api[cli]      # CLI tool
pip install boj-ts-api[pandas,cli]  # both
```

## Quick Start

```python
from boj_ts_api import BOJClient

with BOJClient(lang="en") as client:
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
from boj_ts_api import AsyncBOJClient

async def main():
    async with AsyncBOJClient(lang="en") as client:
        resp = await client.get_data_code(db="CO", code="TK99F1000601GCQ01000")
        print(resp.RESULTSET[0].VALUES.VALUES)

asyncio.run(main())
```

### CSV + pandas

```python
from boj_ts_api import BOJClient, csv_to_dataframe

with BOJClient(lang="en") as client:
    csv_text = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")
    df = csv_to_dataframe(csv_text)
    print(df.head())
```

### CLI

```bash
bojts get-data-code --db CO --code TK99F1000601GCQ01000
bojts get-metadata --db FM08 --format csv
bojts --lang jp get-data-layer --db FM08 --frequency D --layer "1,1"
```

## API Endpoints

| Method | Endpoint | Client Method |
|--------|----------|---------------|
| Code API | `/api/v1/getDataCode` | `get_data_code()`, `iter_data_code()`, `get_data_code_csv()` |
| Layer API | `/api/v1/getDataLayer` | `get_data_layer()`, `iter_data_layer()`, `get_data_layer_csv()` |
| Metadata API | `/api/v1/getMetadata` | `get_metadata()`, `get_metadata_csv()` |

## Documentation

Full documentation: [https://obichan117.github.io/boj-ts-api/](https://obichan117.github.io/boj-ts-api/)

## License

MIT
