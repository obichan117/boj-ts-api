# boj-ts-api

Generic Python client for the [Bank of Japan Time-Series Statistics API](https://www.stat-search.boj.or.jp/).

[![PyPI](https://img.shields.io/pypi/v/boj-ts-api)](https://pypi.org/project/boj-ts-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Low-level, typed wrapper around the three BOJ API endpoints. For a beginner-friendly interface with domain wrappers and enum-driven filtering, see [pyboj](https://github.com/obichan117/pyboj).

## Installation

```bash
pip install boj-ts-api
```

## Usage

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
        print(series.SERIES_CODE, series.VALUES.VALUES)
```

### Auto-Pagination

```python
with Client(lang=Lang.EN) as client:
    for series in client.iter_data_code(db="CO", code="TK99F1000601GCQ01000"):
        print(series.SERIES_CODE, len(series.VALUES.SURVEY_DATES), "data points")
```

### Fetch Data by Layer

```python
from boj_ts_api import Client, Frequency, Lang

with Client(lang=Lang.EN) as client:
    resp = client.get_data_layer(db="FM08", frequency=Frequency.D, layer="1,1")
    for series in resp.RESULTSET:
        print(series.SERIES_CODE, series.VALUES.VALUES[:5])
```

### Metadata

```python
with Client(lang=Lang.EN) as client:
    meta = client.get_metadata(db="FM08")
    for rec in meta.RESULTSET[:3]:
        print(rec.SERIES_CODE, rec.FREQUENCY, rec.NAME_OF_TIME_SERIES)
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

### CSV Output

```python
with Client(lang=Lang.EN) as client:
    csv_text = client.get_data_code_csv(db="CO", code="TK99F1000601GCQ01000")
    print(csv_text)
```

## API Surface

| Method | Description |
|--------|-------------|
| `get_data_code()` | Fetch time-series data by series code(s) |
| `iter_data_code()` | Auto-paginating iterator over series results |
| `get_data_code_csv()` | Fetch data as raw CSV text |
| `get_data_layer()` | Fetch data by hierarchy layer |
| `iter_data_layer()` | Auto-paginating iterator for layer data |
| `get_data_layer_csv()` | Fetch layer data as raw CSV text |
| `get_metadata()` | Fetch series metadata for a database |
| `get_metadata_csv()` | Fetch metadata as raw CSV text |

Both `Client` (sync) and `AsyncClient` (async) expose the same methods.

## License

MIT
