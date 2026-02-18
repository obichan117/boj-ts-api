# Upstream BOJ API Reference

This page documents the **Bank of Japan Time-Series Statistics API** — the upstream REST API that `boj-ts-api` wraps.

!!! info "Official Sources"
    - [API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm) — original BOJ notice
    - [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/) — interactive search UI
    - [OpenAPI Specification](https://github.com/obichan117/boj-ts-api/blob/main/openapi.yaml) — machine-readable spec

## Base URL

```
https://www.stat-search.boj.or.jp
```

## Authentication

No authentication required. The API is publicly accessible.

## Endpoints

### GET `/api/v1/getDataCode`

Fetch time-series data by **series code(s)**.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier (e.g. `CO`, `FM08`) |
| `code` | string | Yes | Series code(s), comma-separated for multiple |
| `format` | string | Yes | Response format: `json` or `csv` |
| `lang` | string | Yes | Language: `jp` or `en` |
| `startDate` | string | No | Start date (format depends on frequency, e.g. `202401` for monthly) |
| `endDate` | string | No | End date |
| `startPosition` | integer | No | Pagination offset (from `NEXTPOSITION` in previous response) |

### GET `/api/v1/getDataLayer`

Fetch time-series data by **hierarchy layer** (browse by category tree).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier |
| `frequency` | string | Yes | Frequency code: `CY`, `FY`, `CH`, `FH`, `Q`, `M`, `W`, `D` |
| `layer` | string | Yes | Comma-separated layer path (e.g. `1,1` for layer1=1, layer2=1) |
| `format` | string | Yes | Response format: `json` or `csv` |
| `lang` | string | Yes | Language: `jp` or `en` |
| `startDate` | string | No | Start date |
| `endDate` | string | No | End date |
| `startPosition` | integer | No | Pagination offset |

### GET `/api/v1/getMetadata`

Fetch metadata (series catalogue) for a database.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier |
| `format` | string | Yes | Response format: `json` or `csv` |
| `lang` | string | Yes | Language: `jp` or `en` |

## Response Format (JSON)

All JSON responses share an envelope structure:

```json
{
  "STATUS": 200,
  "MESSAGEID": "",
  "MESSAGE": "",
  "DATE": "2026-02-18T13:00:00.000+09:00",
  "PARAMETER": { ... },
  "NEXTPOSITION": null,
  "RESULTSET": [ ... ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `STATUS` | integer | `200` on success, `400`/`500` on error |
| `MESSAGEID` | string | Error code (e.g. `E0001`) when STATUS is not 200 |
| `MESSAGE` | string | Human-readable error message |
| `DATE` | string | Server timestamp (ISO 8601 with timezone) |
| `PARAMETER` | object | Echo of the request parameters |
| `NEXTPOSITION` | integer or null | Pagination cursor; `null` means last page |
| `RESULTSET` | array | Array of result objects (varies by endpoint) |

### Data Result Object (getDataCode / getDataLayer)

```json
{
  "SERIES_CODE": "TK99F1000601GCQ01000",
  "NAME_OF_TIME_SERIES": "All Items, Ku-area of Tokyo",
  "NAME_OF_TIME_SERIES_J": "東京都区部 総合",
  "UNIT": "CY2020=100",
  "UNIT_J": "2020年=100",
  "FREQUENCY": "M",
  "CATEGORY": "Consumer Price Index",
  "CATEGORY_J": "消費者物価指数",
  "LAST_UPDATE": 20250520,
  "VALUES": {
    "SURVEY_DATES": [202401, 202402, 202403, 202404],
    "VALUES": [106.9, 106.8, 107.2, 107.5]
  }
}
```

### Metadata Result Object (getMetadata)

```json
{
  "SERIES_CODE": "FM08'MAINAVG",
  "NAME_OF_TIME_SERIES": "Call Rates (Uncollateralized Overnight)/Average",
  "NAME_OF_TIME_SERIES_J": "コールレート(無担保オーバーナイト物)/平均",
  "UNIT": "% per annum",
  "UNIT_J": "年利率%",
  "FREQUENCY": "D",
  "CATEGORY": "Financial Markets",
  "CATEGORY_J": "金融市場",
  "LAYER1": "1",
  "LAYER2": "1",
  "LAYER3": null,
  "LAYER4": null,
  "LAYER5": null,
  "START_OF_THE_TIME_SERIES": "19850701",
  "END_OF_THE_TIME_SERIES": "20251128",
  "LAST_UPDATE": 20251201,
  "UNIT_NOTES": null,
  "UNIT_NOTES_J": null,
  "NOTES": "Source: BOJ",
  "NOTES_J": "出所：日本銀行"
}
```

## Frequency Codes

| Code | Meaning |
|------|---------|
| `CY` | Calendar Year |
| `FY` | Fiscal Year (April–March) |
| `CH` | Calendar Half |
| `FH` | Fiscal Half |
| `Q` | Quarterly |
| `M` | Monthly |
| `W` | Weekly |
| `D` | Daily |

## Date Formats

The `startDate` / `endDate` format depends on the series frequency:

| Frequency | Format | Example |
|-----------|--------|---------|
| CY, FY | `YYYY` | `2024` |
| CH, FH | `YYYYH` | `20241` (first half) |
| Q | `YYYYQ` | `20241` (Q1) |
| M | `YYYYMM` | `202401` (January) |
| W, D | `YYYYMMDD` | `20240115` |

`SURVEY_DATES` values in responses follow the same pattern as integers (e.g. `202401` for monthly).

## Pagination

When a response contains more data than fits in one page, `NEXTPOSITION` will be a non-null integer. Pass this value as the `startPosition` parameter in the next request to fetch the next page.

## API Limits

| Limit | Value |
|-------|-------|
| Max series per Code request | 250 |
| Max data points per request | 60,000 |
| Max series per Layer request | 1,250 |

## Error Responses

When `STATUS` is not `200`, the response includes an error code and message:

```json
{
  "STATUS": 400,
  "MESSAGEID": "E0001",
  "MESSAGE": "Required parameter 'db' is missing.",
  "DATE": "2026-02-18T15:00:00.000+09:00",
  "PARAMETER": null,
  "NEXTPOSITION": null,
  "RESULTSET": []
}
```

Note that the HTTP status code is always `200` — errors are indicated by the `STATUS` field in the JSON body.

## Contact

BOJ Economic Statistics Division: post.rsd17@boj.or.jp
