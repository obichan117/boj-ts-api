# API Reference

## High-Level Client

### BOJ

::: pyboj._boj.BOJ
    options:
      members:
        - __init__
        - close
        - metadata
        - exchange_rates
        - interest_rates
        - price_indices
        - tankan
        - balance_of_payments
        - money_deposits
        - loans
        - financial_markets
        - balance_sheets
        - flow_of_funds
        - boj_operations
        - public_finance
        - international

### Database Enum

::: pyboj._config.Database

---

## Domain Wrappers

### Base

::: pyboj._domains._base.Series
    options:
      members:
        - series_code
        - name
        - name_jp
        - unit
        - frequency
        - category
        - dates
        - values
        - to_dataframe

### ExchangeRate

::: pyboj._domains.exchange_rate.ExchangeRate

::: pyboj._domains.exchange_rate.Currency

::: pyboj._domains.exchange_rate.RateType

### InterestRate

::: pyboj._domains.interest_rate.InterestRate

::: pyboj._domains.interest_rate.RateCategory

::: pyboj._domains.interest_rate.Collateralization

### PriceIndex

::: pyboj._domains.price_index.PriceIndex

::: pyboj._domains.price_index.IndexType

### Tankan

::: pyboj._domains.tankan.Tankan

::: pyboj._domains.tankan.TankanIndustry

::: pyboj._domains.tankan.TankanSize

::: pyboj._domains.tankan.TankanItem

::: pyboj._domains.tankan.TankanSeriesType

::: pyboj._domains.tankan.TankanTiming

### BalanceOfPayments

::: pyboj._domains.balance_of_payments.BalanceOfPayments

::: pyboj._domains.balance_of_payments.BopAccount

### MoneyDeposit

::: pyboj._domains.money_deposit.MoneyDeposit

::: pyboj._domains.money_deposit.MonetaryComponent

::: pyboj._domains.money_deposit.Adjustment

### Loan

::: pyboj._domains.loan.Loan

::: pyboj._domains.loan.IndustrySector

---

## Low-Level Clients

### Synchronous

::: boj_ts_api.client.Client
    options:
      members:
        - get_data_code
        - iter_data_code
        - get_data_code_csv
        - get_data_layer
        - iter_data_layer
        - get_data_layer_csv
        - get_metadata
        - get_metadata_csv
        - close

### Asynchronous

::: boj_ts_api.async_client.AsyncClient
    options:
      members:
        - get_data_code
        - iter_data_code
        - get_data_code_csv
        - get_data_layer
        - iter_data_layer
        - get_data_layer_csv
        - get_metadata
        - get_metadata_csv
        - close

## Response Models

::: boj_ts_api._types.models.response.DataResponse

::: boj_ts_api._types.models.response.MetadataResponse

::: boj_ts_api._types.models.series.SeriesResult

::: boj_ts_api._types.models.series.SeriesValues

::: boj_ts_api._types.models.metadata.MetadataRecord

## Enums

::: boj_ts_api._types.config.Lang

::: boj_ts_api._types.config.Format

::: boj_ts_api._types.config.Frequency

## Exceptions

::: boj_ts_api._types.exceptions.BOJError

::: boj_ts_api._types.exceptions.BOJAPIError

::: boj_ts_api._types.exceptions.BOJRequestError

::: boj_ts_api._types.exceptions.BOJValidationError

## Utilities

::: pyboj._helpers.csv.csv_to_dataframe
