#!env python3
from typing import Optional

import typer
import trio
from rich.console import Console
from toolbox.dumper import queue_downloads, DumperProgress
from toolbox.mtg_vars import expansions


def main(
        exps_input: Optional[str] = typer.Argument(None),
        all_exps: bool = typer.Option(False, "--all"),
):
    selected_expansions = sorted(expansions)
    if exps_input:
        selected_expansions = sorted(exp.strip() for exp in exps_input.split(","))
    elif not all_exps:
        typer.echo("Plese specify expansions or use --all")
        raise typer.Exit()

    trio.run(queue_downloads, selected_expansions, instruments=[DumperProgress()])


if __name__ == "__main__":
    typer.run(main)
