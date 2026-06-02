"""Terminal report rendering using Rich.

This module formats and prints the organization results into a clean, modern
TUI layout complying with the design system specifications.
"""

from collections import defaultdict
from pathlib import Path

from rich.box import ROUNDED
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from autofileorganizer.categories import CATEGORY_ICONS
from autofileorganizer.organizer import OrganizationReport


def print_report(report: OrganizationReport, console: Console = None) -> None:
    """Print a styled summary and details of the organization report.

    Args:
        report: The OrganizationReport to display.
        console: Optional Rich Console to use for printing.
    """
    if console is None:
        console = Console()

    # Title Banner
    mode_text = (
        "[bold #F59E0B]🔍 SIMULATION MODE (DRY-RUN)[/]"
        if report.dry_run
        else "[bold #2563EB]🚀 ORGANIZATION COMPLETE[/]"
    )
    console.print()
    console.print(
        Panel.fit(
            f"  {mode_text}  \n"
            f"[#E5E7EB]Target directory: [italic]{report.target_dir}[/][/]",
            border_style="#2563EB" if not report.dry_run else "#F59E0B",
            box=ROUNDED,
        )
    )

    # 1. If dry-run or verbosity, list individual file movements
    if report.moved_files:
        console.print("\n[bold #E5E7EB]File move details :[/]")
        for src, dest, cat in report.moved_files:
            icon = CATEGORY_ICONS.get(cat, "📁")
            try:
                # Try to use relative paths for readability
                rel_src = src.relative_to(report.target_dir)
            except ValueError:
                rel_src = src

            try:
                rel_dest = dest.relative_to(report.target_dir)
            except ValueError:
                rel_dest = dest

            console.print(
                f"  {icon} [dim]{rel_src}[/] [#2563EB]→[/] [#16A34A]{rel_dest}[/]"
            )

    # List failures if any
    if report.failed_files:
        console.print("\n[bold #DC2626]⚠️ Errors encountered :[/]")
        for src, err in report.failed_files:
            try:
                rel_src = src.relative_to(report.target_dir)
            except ValueError:
                rel_src = src
            console.print(f"  ❌ [#E5E7EB]{rel_src}[/] : [italic #DC2626]{err}[/]")

    # 2. Rich Table for category summary
    category_counts: dict[str, int] = defaultdict(int)
    category_destinations: dict[str, Path] = {}

    for _, dest, cat in report.moved_files:
        category_counts[cat] += 1
        category_destinations[cat] = dest.parent

    table = Table(
        title="\n[bold #E5E7EB]Category Summary[/]",
        box=ROUNDED,
        border_style="#2563EB",
        header_style="bold #2563EB",
    )
    table.add_column("Category", style="bold #E5E7EB", width=20)
    table.add_column("Files Count", justify="right", style="#16A34A")
    table.add_column("Destination", style="dim #E5E7EB")

    # Add rows for categories that have at least one file organized
    sorted_categories = sorted(
        category_counts.keys(), key=lambda x: category_counts[x], reverse=True
    )
    for cat in sorted_categories:
        count = category_counts[cat]
        icon = CATEGORY_ICONS.get(cat, "📁")
        dest_path = category_destinations.get(cat)
        try:
            rel_dest = dest_path.relative_to(report.target_dir) if dest_path else ""
        except ValueError:
            rel_dest = str(dest_path) if dest_path else ""

        table.add_row(f"{icon} {cat}", str(count), f"{rel_dest}/")

    if report.moved_files:
        console.print(table)
    else:
        console.print("\n[italic #F59E0B]No files to organize.[/]")

    # 3. Overall Execution Summary
    summary_lines = [
        f"  [bold #E5E7EB]Total Scanned :[/] [bold]{report.total_scanned}[/]",
        f"  [bold #E5E7EB]Total Moved :[/] [bold #16A34A]{report.total_moved}[/]",
    ]
    if report.total_failed > 0:
        summary_lines.append(
            f"  [bold #E5E7EB]Failures :[/] [bold #DC2626]{report.total_failed}[/]"
        )
    summary_lines.append(
        f"  [bold #E5E7EB]Execution Duration :[/] "
        f"[italic #F59E0B]{report.execution_duration:.3f}s[/]"
    )

    console.print()
    console.print(
        Panel(
            "\n".join(summary_lines),
            title="[bold #2563EB]Statistics[/]",
            border_style="#2563EB",
            box=ROUNDED,
            expand=False,
        )
    )
    console.print()
