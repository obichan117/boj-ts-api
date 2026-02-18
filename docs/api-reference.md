# API Reference

## Clients

::: boj_ts_api.client.sync_client.BOJClient
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

::: boj_ts_api.client.async_client.AsyncBOJClient
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

## Models

::: boj_ts_api.models.response.DataResponse

::: boj_ts_api.models.response.MetadataResponse

::: boj_ts_api.models.series.SeriesResult

::: boj_ts_api.models.series.SeriesValues

::: boj_ts_api.models.metadata.MetadataRecord

## Enums

::: boj_ts_api.config.Lang

::: boj_ts_api.config.Format

::: boj_ts_api.config.Frequency

## Exceptions

::: boj_ts_api.exceptions.BOJError

::: boj_ts_api.exceptions.BOJAPIError

::: boj_ts_api.exceptions.BOJRequestError

::: boj_ts_api.exceptions.BOJValidationError

## Utilities

::: boj_ts_api.csv_helper.csv_to_dataframe
