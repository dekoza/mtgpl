#!env python3
from typing import Optional

import appdirs
import httpx
import trio
import typer
from rich.console import Console

from toolbox.dumper import get_bulk_data, queue_downloads, render_wanted
from toolbox.mtg_vars import expansions

BULK_TYPE = "default_cards"
GET_RULINGS = True
APP_ID = "pl.mtgpopolsku.mtgd"

app = typer.Typer()
client = httpx.AsyncClient(timeout=15, http2=True)


@app.command()
def refresh():
    """
    Refresh cached data.
    """
    trio.run(get_bulk_data, client, BULK_TYPE)


@app.command()
def wanted():
    """
    Generate my wanted list.
    """
    trio.run(render_wanted, client)


@app.command(no_args_is_help=True)
def dump(
    exps: Optional[list[str]] = typer.Argument(
        None, help="Space-separated list of expansion codes."
    ),
    all_exps: bool = typer.Option(False, "--all", help="Download ALL expansions."),
):
    """
    Dump selected (or ALL) expansions.
    """
    selected_expansions = expansions if all_exps else exps

    trio.run(queue_downloads, selected_expansions, client)


if __name__ == "__main__":
    app()
