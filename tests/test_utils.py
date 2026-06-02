"""Tests for the utils module."""

from pathlib import Path

from autofileorganizer.utils import resolve_name_conflict


def test_resolve_name_conflict_no_conflict(tmp_path: Path) -> None:
    """Verify filename is unchanged if no conflict exists."""
    filename = "test.txt"
    dest_path = resolve_name_conflict(tmp_path, filename)
    assert dest_path == tmp_path / filename


def test_resolve_name_conflict_with_existing_file(tmp_path: Path) -> None:
    """Verify _1, _2 is appended when files already exist in destination."""
    filename = "test.txt"
    # Create the first conflict file
    (tmp_path / filename).touch()

    dest_path = resolve_name_conflict(tmp_path, filename)
    assert dest_path == tmp_path / "test_1.txt"

    # Create the second conflict file
    (tmp_path / "test_1.txt").touch()
    dest_path = resolve_name_conflict(tmp_path, filename)
    assert dest_path == tmp_path / "test_2.txt"


def test_resolve_name_conflict_with_allocated_paths(tmp_path: Path) -> None:
    """Verify name conflicts are resolved using allocated_paths (dry-run)."""
    filename = "test.txt"
    allocated = {tmp_path / filename, tmp_path / "test_1.txt"}

    dest_path = resolve_name_conflict(tmp_path, filename, allocated_paths=allocated)
    assert dest_path == tmp_path / "test_2.txt"
