"""Command Line Interface for AutoFileOrganizer.

This module exposes the CLI commands and options using Typer, validating
inputs and invoking the core organizer.
"""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from autofileorganizer import __version__
from autofileorganizer.organizer import organize_directory
from autofileorganizer.report import print_report

app = typer.Typer(
    name="autofileorganizer",
    help="AutoFileOrganizer: Organize your files automatically based on categories.",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    """Print the tool version and exit."""
    if value:
        console.print(
            f"[bold #2563EB]AutoFileOrganizer[/] version [bold #16A34A]{__version__}[/]"
        )
        raise typer.Exit()


@app.command()
def main(
    directory: Optional[Path] = typer.Argument(
        None,
        help="The target directory to organize. Defaults to current directory.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        "-r",
        help="Scan and organize subdirectories recursively.",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        "-d",
        help="Simulate the organization without making filesystem changes.",
    ),
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show the version and exit.",
    ),
) -> None:
    """Organize files in the target directory into categorised folders."""
    # Default to current directory if not specified
    if directory is None:
        directory = Path.cwd()

    try:
        report = organize_directory(
            target_dir=directory, recursive=recursive, dry_run=dry_run
        )
        print_report(report, console=console)
    except Exception as e:
        console.print(
            f"[bold #DC2626]Error:[/] Failed to organize directory: {e}"
        )
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
