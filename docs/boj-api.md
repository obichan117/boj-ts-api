# Upstream BOJ API Reference

This page documents the **Bank of Japan Time-Series Statistics API** — the upstream API that `boj-ts-api` wraps.
This reference is based on the [official API manual (PDF, Japanese)](https://www.stat-search.boj.or.jp/info/api_manual.pdf), verified 2026-02-19.

!!! info "Official Sources"
    - [API Manual (PDF, Japanese)](https://www.stat-search.boj.or.jp/info/api_manual.pdf) — authoritative specification
    - [API Usage Notes (PDF)](https://www.stat-search.boj.or.jp/info/api_notice.pdf)
    - [Request URL Helper Tool (Excel)](https://www.stat-search.boj.or.jp/info/api_tool.xlsx)
    - [BOJ API Announcement (2026-02-18)](https://www.boj.or.jp/statistics/outline/notice_2026/not260218a.htm)
    - [BOJ Time-Series Search Site](https://www.stat-search.boj.or.jp/)
    - [OpenAPI Specification (Interactive)](openapi-spec.md)

## API Design: HTTP-RPC, not REST

!!! warning "This is not a REST API"
    Despite using HTTP GET and returning JSON, the BOJ API follows an **HTTP-RPC** pattern
    — think "DB query functions exposed over HTTP" (「DBクエリ関数をHTTPで公開した」形).

    We provide an OpenAPI spec for documentation convenience, but the API does not follow
    REST conventions. Keep this in mind when integrating.

Key non-standard behaviors:

| Behavior | What the BOJ API does | What REST would do |
|----------|----------------------|-------------------|
| **Endpoints** | Verb-based: `getDataCode`, `getDataLayer`, `getMetadata` | Resource-based: `/series/{id}` |
| **HTTP status** | Always `200`, even on errors | `400`, `404`, `500` etc. |
| **Error signaling** | `STATUS` field inside JSON body | HTTP status code |
| **Content negotiation** | `format=json\|csv` query param | `Accept` header |
| **Pagination** | `NEXTPOSITION` in response body | `Link` header or cursor param |
| **Case sensitivity** | Parameters are case-insensitive (names and values) | Case-sensitive by convention |
| **Frequency codes** | Request uses abbreviations (`M`, `D`), response uses full names (`MONTHLY`, `DAILY`) | Consistent format |
| **Date params** | Weekly/daily data uses `YYYYMM` (monthly granularity), not `YYYYMMDD` | Matches data granularity |

## Base URL

```
https://www.stat-search.boj.or.jp
```

## Authentication

No authentication required. The API is publicly accessible.

## General Behavior

- **Parameters are case-insensitive** (both names and values).
- **gzip compression** is supported — set `Accept-Encoding: gzip` for smaller responses.
- **Avoid high-frequency access** — connections may be blocked.
- **Error responses are always JSON**, even when `format=csv` was requested.
- **CSV encoding:** Japanese (`lang=jp`) uses Shift-JIS; English (`lang=en`) uses UTF-8.
- **HTTP status code is always `200`** — errors are indicated by the `STATUS` field in the JSON body.
- Data is updated daily around 8:50 AM JST.

## Endpoints

### GET `/api/v1/getDataCode`

Fetch time-series data by **series code(s)**.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier (e.g. `CO`, `FM08`) |
| `code` | string | Yes | Series code(s), comma-separated. **Max 250.** All must share the same frequency. Do **not** include the DB name prefix (use `MADR1Z@D`, not `IR01'MADR1Z@D`). |
| `format` | string | No | Response format: `json` (default) or `csv` |
| `lang` | string | No | Language: `jp` (default) or `en` |
| `startDate` | string | No | Start date (format depends on frequency — see [Date Formats](#date-formats)) |
| `endDate` | string | No | End date |
| `startPosition` | integer | No | Pagination offset (from `NEXTPOSITION` in previous response) |

### GET `/api/v1/getDataLayer`

Fetch time-series data by **hierarchy layer** (browse by category tree).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier |
| `frequency` | string | Yes | Frequency code: `CY`, `FY`, `CH`, `FH`, `Q`, `M`, `W`, `D`. Weekly subtypes (W0–W6) all use `W`. |
| `layer` | string | Yes | Comma-separated layer path. Layer 1 is required; layers 2–5 are optional. Use `*` as wildcard. Examples: `1,1`, `*`, `1,*,2` |
| `format` | string | No | Response format: `json` (default) or `csv` |
| `lang` | string | No | Language: `jp` (default) or `en` |
| `startDate` | string | No | Start date |
| `endDate` | string | No | End date |
| `startPosition` | integer | No | Pagination offset |

### GET `/api/v1/getMetadata`

Fetch metadata (series catalogue) for a database. Does **not** support `startDate`, `endDate`, or `startPosition`.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `db` | string | Yes | Database identifier |
| `format` | string | No | Response format: `json` (default) or `csv` |
| `lang` | string | No | Language: `jp` (default) or `en` |

## Database Codes

| Category | Code | Name (Japanese) |
|----------|------|-----------------|
| Interest Rates | `IR01` | 基準割引率および基準貸付利率 |
| | `IR02` | 預金種類別店頭表示金利の平均年利率等 |
| | `IR03` | 定期預金の預入期間別平均金利 |
| | `IR04` | 貸出約定平均金利 |
| Financial Markets | `FM01` | 無担保コールO/N物レート（毎営業日） |
| | `FM02` | 短期金融市場金利 |
| | `FM03` | 短期金融市場残高 |
| | `FM04` | コール市場残高 |
| | `FM05` | 公社債発行・償還および現存額 |
| | `FM06` | 公社債消化状況（利付国債） |
| | `FM07` | 国債窓口販売額・窓口販売率 |
| | `FM08` | 外国為替市況 |
| | `FM09` | 実効為替レート |
| Money & Deposits | `MD01` | マネタリーベース |
| | `MD02` | マネーストック |
| | `MD03` | マネタリーサーベイ |
| | `MD04` | マネーサプライ（参考） |
| | `MD05` | 通貨流通高 |
| | `MD06` | 日銀当座預金増減要因と金融調節 |
| | `MD07` | 準備預金額 |
| | `MD08` | 業態別の日銀当座預金残高 |
| | `MD09` | マネタリーベースと日本銀行の取引 |
| | `MD10` | 預金者別預金 |
| | `MD11` | 預金・現金・貸出金 |
| | `MD12` | 都道府県別預金・現金・貸出金 |
| | `MD13` | 貸出・預金動向 |
| | `MD14` | 定期預金の残高および新規受入高 |
| Loans | `LA01` | 貸出先別貸出金 |
| | `LA02` | 日本銀行貸出 |
| | `LA03` | その他貸出残高 |
| | `LA04` | コミットメントライン契約額・利用額 |
| | `LA05` | 主要銀行貸出動向アンケート調査 |
| Balance Sheets | `BS01` | 日本銀行勘定 |
| | `BS02` | 民間金融機関の資産・負債 |
| Flow of Funds | `FF` | 資金循環 |
| BOJ Operations | `OB01` | 日本銀行の対政府取引 |
| | `OB02` | 日本銀行が受入れている担保の残高 |
| TANKAN | `CO` | 短観 |
| Prices | `PR01` | 企業物価指数 |
| | `PR02` | 企業向けサービス価格指数 |
| | `PR03` | 製造業部門別投入・産出物価指数 |
| | `PR04` | 最終需要・中間需要物価指数 |
| Public Finance | `PF01` | 財政資金収支 |
| | `PF02` | 政府債務 |
| Balance of Payments | `BP01` | 国際収支統計 |
| BIS/International | `BIS` | BIS国際資金取引統計および国際与信統計 |
| | `DER` | デリバティブ取引に関する定例市場報告 |
| Settlement | `PS01` | 各種決済 |
| | `PS02` | フェイルの発生状況 |
| Other | `OT` | その他 |

## Response Format (JSON)

All JSON responses share an envelope structure:

```json
{
  "STATUS": 200,
  "MESSAGEID": "M181000I",
  "MESSAGE": "正常に終了しました。",
  "DATE": "2026-02-18T13:00:00.000+09:00",
  "PARAMETER": { ... },
  "NEXTPOSITION": null,
  "RESULTSET": [ ... ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `STATUS` | integer | `200` on success, `400` on parameter error, `500` on unexpected error, `503` on database access error |
| `MESSAGEID` | string | Message code (e.g. `M181000I` for success — see [Error Codes](#error-codes)) |
| `MESSAGE` | string | Human-readable message |
| `DATE` | string | Server timestamp in Japan time. For Metadata API, this is the internal data creation time, not request time. |
| `PARAMETER` | object | Echo of the request parameters. `null` on error. |
| `NEXTPOSITION` | integer or null | Pagination cursor; `null` means last page |
| `RESULTSET` | array | Array of result objects (varies by endpoint) |

### Data Result Object (getDataCode / getDataLayer)

```json
{
  "SERIES_CODE": "TK99F1000601GCQ01000",
  "NAME_OF_TIME_SERIES": "All Items, Ku-area of Tokyo",
  "UNIT": "CY2020=100",
  "FREQUENCY": "MONTHLY",
  "CATEGORY": "Consumer Price Index",
  "LAST_UPDATE": 20250520,
  "VALUES": {
    "SURVEY_DATES": [202401, 202402, 202403, 202404],
    "VALUES": [106.9, 106.8, 107.2, 107.5]
  }
}
```

!!! note "Language-dependent fields"
    When `lang=en`: `NAME_OF_TIME_SERIES`, `UNIT`, `CATEGORY` are present.
    When `lang=jp`: `NAME_OF_TIME_SERIES_J`, `UNIT_J`, `CATEGORY_J` are present.
    Fields for the other language are omitted.

### Metadata Result Object (getMetadata)

```json
{
  "SERIES_CODE": "MAINAVG",
  "NAME_OF_TIME_SERIES": "Call Rates (Uncollateralized Overnight)/Average",
  "UNIT": "% per annum",
  "FREQUENCY": "DAILY",
  "CATEGORY": "Financial Markets",
  "LAYER1": "1",
  "LAYER2": "1",
  "LAYER3": null,
  "LAYER4": null,
  "LAYER5": null,
  "START_OF_THE_TIME_SERIES": "19850701",
  "END_OF_THE_TIME_SERIES": "20251128",
  "LAST_UPDATE": 20251201,
  "NOTES": "Source: BOJ"
}
```

## Frequency Codes

### Request Parameter Values

| Code | Meaning |
|------|---------|
| `CY` | Calendar Year |
| `FY` | Fiscal Year (April–March) |
| `CH` | Calendar Half |
| `FH` | Fiscal Half |
| `Q` | Quarterly |
| `M` | Monthly |
| `W` | Weekly (covers W0–W6 subtypes) |
| `D` | Daily |

### Response Field Values

Response `FREQUENCY` fields use **full names**, not the abbreviated codes above:

| Response Value | Meaning |
|----------------|---------|
| `ANNUAL` | Calendar Year |
| `ANNUAL(MAR)` | Fiscal Year |
| `SEMIANNUAL` | Calendar Half |
| `SEMIANNUAL(SEP)` | Fiscal Half |
| `QUARTERLY` | Quarterly |
| `MONTHLY` | Monthly |
| `WEEKLY(MONDAY)` | Weekly (Monday) — also `WEEKLY(TUESDAY)` through `WEEKLY(SUNDAY)` |
| `DAILY` | Daily |

## Date Formats

### Request Parameters (`startDate` / `endDate`)

| Frequency | Format | Example |
|-----------|--------|---------|
| CY, FY | `YYYY` | `2024` |
| CH, FH | `YYYYHH` (HH = 01 or 02) | `202501` (first half) |
| Q | `YYYYQQ` (QQ = 01–04) | `202502` (Q2) |
| M, W, D | `YYYYMM` | `202401` (January) |

!!! warning "Weekly and daily dates use YYYYMM"
    Even though weekly/daily data has day-level granularity, the `startDate` and `endDate`
    parameters use **monthly** format (`YYYYMM`), not `YYYYMMDD`.

Valid date range: **1850–2050**.

### Response Values (`SURVEY_DATES`, `START_OF_THE_TIME_SERIES`, `END_OF_THE_TIME_SERIES`)

| Frequency | Format | Example |
|-----------|--------|---------|
| CY, FY | `YYYY` | `2024` |
| CH, FH | `YYYYHH` | `202501` |
| Q | `YYYYQQ` | `202502` |
| M | `YYYYMM` | `202401` |
| W, D | `YYYYMMDD` | `20240115` |

## Pagination

When a response contains more data than fits in one page, `NEXTPOSITION` will be a non-null integer. Pass this value as the `startPosition` parameter in the next request to fetch the next page.

- **Code API:** `startPosition` is the 1-based index into the list of requested series codes.
- **Layer API:** `startPosition` is a global sequence number across all series in the database (ordered by layer hierarchy).

Pagination is triggered when **either** the series count **or** the data point count exceeds the limit.

## API Limits

| Limit | Value |
|-------|-------|
| Max series per Code request | 250 |
| Max data points per request (series x periods) | 60,000 |
| Max series per Layer request (pre-frequency-filter) | 1,250 |

!!! note "Layer API series counting"
    The 1,250-series limit for Layer API is counted **before** frequency filtering.
    If the specified layers contain 1,300 series across all frequencies but only 800
    match your `frequency` parameter, the request still fails because 1,300 > 1,250.

## Error Codes

| STATUS | MESSAGEID | Message | Description |
|--------|-----------|---------|-------------|
| 200 | `M181000I` | 正常に終了しました。 | Success (may include `null` values for missing data) |
| 200 | `M181030I` | 正常に終了しましたが、該当データはありませんでした。 | Success, but no matching data found |
| 400 | `M181001E` | Invalid input parameters | Invalid characters (`< > " ! \| \ ; '`) or full-width characters, or DB prefix in code |
| 400 | `M181002E` | Invalid language setting | |
| 400 | `M181003E` | 結果ファイル形式が正しくありません。 | Invalid format parameter |
| 400 | `M181004E` | DBが指定されていません。 | Missing `db` parameter |
| 400 | `M181005E` | DB名が正しくありません。 | Invalid database name |
| 400 | `M181006E` | 系列コードが指定されていません。 | Missing `code` parameter |
| 400 | `M181007E` | 系列コードの数が1250を超えています。 | Too many series codes |
| 400 | `M181008E` | 指定した開始期が正しくありません。 | Invalid start date |
| 400 | `M181009E` | 指定した終了期が正しくありません。 | Invalid end date |
| 400 | `M181010E` | 時期は1850年から2050年までを数値で指定してください。 | Date out of valid range (1850–2050) |
| 400 | `M181011E` | 開始期と終了期の順序を正しく指定してください。 | Start date > end date |
| 400 | `M181012E` | 検索開始位置が正しくありません。 | Invalid startPosition (must be integer >= 1) |
| 400 | `M181013E` | 指定した系列コードは存在しません。：*番目のコード | Series code not found (with position) |
| 400 | `M181014E` | 指定した系列コードの期種が一致しません。：*番目のコード | Frequency mismatch between codes |
| 400 | `M181015E` | 指定した開始期の設定形式が期種と一致しません。 | Start date format doesn't match frequency |
| 400 | `M181016E` | 指定した終了期の設定形式が期種と一致しません。 | End date format doesn't match frequency |
| 400 | `M181017E` | 期種が指定されていません。 | Missing frequency (Layer API) |
| 400 | `M181018E` | 期種が正しくありません。 | Invalid frequency code |
| 400 | `M181019E` | 階層情報が指定されていません。 | Missing layer (Layer API). Layer 1 is required. |
| 400 | `M181020E` | 階層情報設定が正しくありません。 | Invalid layer specification |
| 500 | `M181090S` | 予期しないエラーが発生しました。 | Unexpected server error |
| 503 | `M181091S` | データベースにアクセス中にエラーになりました。 | Database access error |

## Contact

BOJ Economic Statistics Division: post.rsd17@boj.or.jp
