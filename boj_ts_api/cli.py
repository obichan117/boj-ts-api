"""CLI interface for the BOJ Time-Series API.

Install with: ``pip install boj-ts-api[cli]``

Usage::

    bojts get-data-code --db CO --code TK99F1000601GCQ01000
    bojts get-data-layer --db FM08 --frequency D --layer "1,1"
    bojts get-metadata --db FM08
"""

from __future__ import annotations

import json
import sys

try:
    import click
except ImportError:
    sys.exit("click is required for the CLI. Install with: pip install boj-ts-api[cli]")

from boj_ts_api.client.sync_client import BOJClient
from boj_ts_api.exceptions import BOJError


@click.group()
@click.option("--lang", default="en", type=click.Choice(["en", "jp"]), help="Response language.")
@click.pass_context
def main(ctx: click.Context, lang: str) -> None:
    """BOJ Time-Series Statistics API client."""
    ctx.ensure_object(dict)
    ctx.obj["lang"] = lang


@main.command("get-data-code")
@click.option("--db", required=True, help="Database name (e.g. CO, FM08).")
@click.option("--code", required=True, help="Series code(s), comma-separated.")
@click.option("--start-date", default=None, help="Start date (YYYYMM or YYYY).")
@click.option("--end-date", default=None, help="End date (YYYYMM or YYYY).")
@click.option(
    "--format",
    "fmt",
    default="json",
    type=click.Choice(["json", "csv"]),
    help="Output format.",
)
@click.pass_context
def get_data_code(
    ctx: click.Context,
    db: str,
    code: str,
    start_date: str | None,
    end_date: str | None,
    fmt: str,
) -> None:
    """Fetch time-series data by series code."""
    lang = ctx.obj["lang"]
    try:
        with BOJClient(lang=lang) as client:
            if fmt == "csv":
                text = client.get_data_code_csv(
                    db=db, code=code, start_date=start_date, end_date=end_date
                )
                click.echo(text)
            else:
                resp = client.get_data_code(
                    db=db, code=code, start_date=start_date, end_date=end_date
                )
                click.echo(json.dumps(resp.model_dump(), indent=2, ensure_ascii=False))
    except BOJError as exc:
        raise click.ClickException(str(exc)) from exc


@main.command("get-data-layer")
@click.option("--db", required=True, help="Database name.")
@click.option("--frequency", required=True, help="Frequency (CY,FY,CH,FH,Q,M,W,D).")
@click.option("--layer", required=True, help="Layer specification, comma-separated.")
@click.option("--start-date", default=None, help="Start date.")
@click.option("--end-date", default=None, help="End date.")
@click.option(
    "--format",
    "fmt",
    default="json",
    type=click.Choice(["json", "csv"]),
    help="Output format.",
)
@click.pass_context
def get_data_layer(
    ctx: click.Context,
    db: str,
    frequency: str,
    layer: str,
    start_date: str | None,
    end_date: str | None,
    fmt: str,
) -> None:
    """Fetch time-series data by hierarchy layer."""
    lang = ctx.obj["lang"]
    try:
        with BOJClient(lang=lang) as client:
            if fmt == "csv":
                text = client.get_data_layer_csv(
                    db=db, frequency=frequency, layer=layer,
                    start_date=start_date, end_date=end_date,
                )
                click.echo(text)
            else:
                resp = client.get_data_layer(
                    db=db, frequency=frequency, layer=layer,
                    start_date=start_date, end_date=end_date,
                )
                click.echo(json.dumps(resp.model_dump(), indent=2, ensure_ascii=False))
    except BOJError as exc:
        raise click.ClickException(str(exc)) from exc


@main.command("get-metadata")
@click.option("--db", required=True, help="Database name.")
@click.option(
    "--format",
    "fmt",
    default="json",
    type=click.Choice(["json", "csv"]),
    help="Output format.",
)
@click.pass_context
def get_metadata(ctx: click.Context, db: str, fmt: str) -> None:
    """Fetch metadata for a database."""
    lang = ctx.obj["lang"]
    try:
        with BOJClient(lang=lang) as client:
            if fmt == "csv":
                text = client.get_metadata_csv(db=db)
                click.echo(text)
            else:
                resp = client.get_metadata(db=db)
                click.echo(json.dumps(resp.model_dump(), indent=2, ensure_ascii=False))
    except BOJError as exc:
        raise click.ClickException(str(exc)) from exc
