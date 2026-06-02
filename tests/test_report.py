"""Tests for the report module."""

from pathlib import Path

from rich.console import Console

from autofileorganizer.organizer import OrganizationReport
from autofileorganizer.report import print_report


def test_print_report_dry_run() -> None:
    """Verify print_report output for a dry-run report."""
    console = Console(record=True, width=100)
    report = OrganizationReport(
        target_dir=Path("/dummy/path"),
        dry_run=True,
        total_scanned=2,
        moved_files=[
            (
                Path("/dummy/path/pic.png"),
                Path("/dummy/path/Images/pic.png"),
                "Images",
            ),
            (
                Path("/dummy/path/doc.pdf"),
                Path("/dummy/path/Documents/doc.pdf"),
                "Documents",
            ),
        ],
        failed_files=[
            (Path("/dummy/path/err.txt"), "Access Denied"),
        ],
        execution_duration=0.045,
    )

    print_report(report, console=console)
    output = console.export_text()

    assert "SIMULATION MODE" in output
    assert "Target directory: /dummy/path" in output
    assert "pic.png" in output
    assert "Images/pic.png" in output
    assert "doc.pdf" in output
    assert "Documents/doc.pdf" in output
    assert "Errors encountered" in output
    assert "Access Denied" in output
    assert "Total Scanned : 2" in output
    assert "Total Moved : 2" in output
    assert "Failures : 1" in output
    assert "Execution Duration" in output


def test_print_report_empty() -> None:
    """Verify print_report output for an empty report."""
    console = Console(record=True, width=100)
    report = OrganizationReport(
        target_dir=Path("/dummy/path"),
        dry_run=False,
        total_scanned=0,
        moved_files=[],
        failed_files=[],
        execution_duration=0.001,
    )

    print_report(report, console=console)
    output = console.export_text()

    assert "ORGANIZATION COMPLETE" in output
    assert "No files to organize" in output
    assert "Total Scanned : 0" in output
    assert "Total Moved : 0" in output
    assert "Failures" not in output
