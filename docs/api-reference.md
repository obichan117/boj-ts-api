# API Reference

## Clients

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
