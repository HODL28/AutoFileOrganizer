"""Tests for the organizer module."""

from pathlib import Path

import pytest

from autofileorganizer.organizer import organize_directory


def test_organize_directory_dry_run(tmp_path: Path) -> None:
    """Verify dry-run simulates movement without modifying disk."""
    # Setup test files
    file1 = tmp_path / "photo.jpg"
    file2 = tmp_path / "doc.pdf"
    file1.touch()
    file2.touch()

    report = organize_directory(tmp_path, recursive=False, dry_run=True)

    assert report.total_scanned == 2
    assert report.total_moved == 2
    assert report.total_failed == 0
    assert report.dry_run is True

    # Files must still exist in original location
    assert file1.exists()
    assert file2.exists()

    # Dest folders must NOT be created
    assert not (tmp_path / "Images").exists()
    assert not (tmp_path / "Documents").exists()


def test_organize_directory_real_move(tmp_path: Path) -> None:
    """Verify real run moves files and creates directories."""
    file1 = tmp_path / "photo.jpg"
    file2 = tmp_path / "doc.pdf"
    file3 = tmp_path / "other.xyz"
    file1.touch()
    file2.touch()
    file3.touch()

    report = organize_directory(tmp_path, recursive=False, dry_run=False)

    assert report.total_scanned == 3
    assert report.total_moved == 3
    assert report.total_failed == 0
    assert report.dry_run is False

    # Original files must be gone
    assert not file1.exists()
    assert not file2.exists()
    assert not file3.exists()

    # Check destinations
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "Documents" / "doc.pdf").exists()
    assert (tmp_path / "Others" / "other.xyz").exists()


def test_organize_directory_with_conflicts(tmp_path: Path) -> None:
    """Verify organization handles naming conflicts correctly."""
    # Create target directory Images/ and file already inside
    img_dir = tmp_path / "Images"
    img_dir.mkdir()
    existing_file = img_dir / "photo.jpg"
    existing_file.touch()

    # Create root file with same name
    root_file = tmp_path / "photo.jpg"
    root_file.touch()

    report = organize_directory(tmp_path, recursive=False, dry_run=False)

    assert report.total_scanned == 1
    assert report.total_moved == 1

    # Check renamed target
    assert existing_file.exists()
    assert (img_dir / "photo_1.jpg").exists()
    assert not root_file.exists()


def test_organize_directory_error_handling(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Verify that exceptions during moving are caught and logged."""
    file1 = tmp_path / "photo.jpg"
    file1.touch()

    # Monkeypatch Path.rename to raise an OSError
    def mock_rename(*args, **kwargs):
        raise OSError("Permission denied")

    monkeypatch.setattr(Path, "rename", mock_rename)

    report = organize_directory(tmp_path, recursive=False, dry_run=False)

    assert report.total_scanned == 1
    assert report.total_moved == 0
    assert report.total_failed == 1

    src, err = report.failed_files[0]
    assert src == file1
    assert "Permission denied" in err
