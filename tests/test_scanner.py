"""Tests for the scanner module."""

from contextlib import suppress
from pathlib import Path

from autofileorganizer.scanner import scan_directory


def test_scan_directory_simple(tmp_path: Path) -> None:
    """Verify that normal files are scanned."""
    (tmp_path / "file1.jpg").touch()
    (tmp_path / "file2.pdf").touch()

    # Subdirectory with file (not recursive)
    sub = tmp_path / "subdir"
    sub.mkdir()
    (sub / "file3.txt").touch()

    files = scan_directory(tmp_path, recursive=False)
    # Convert to filenames for easy assert
    names = {f.name for f in files}
    assert names == {"file1.jpg", "file2.pdf"}


def test_scan_directory_recursive(tmp_path: Path) -> None:
    """Verify that files in subdirectories are scanned in recursive mode."""
    (tmp_path / "file1.jpg").touch()

    sub1 = tmp_path / "subdir1"
    sub1.mkdir()
    (sub1 / "file2.pdf").touch()

    sub2 = sub1 / "subdir2"
    sub2.mkdir()
    (sub2 / "file3.txt").touch()

    files = scan_directory(tmp_path, recursive=True)
    names = {f.name for f in files}
    assert names == {"file1.jpg", "file2.pdf", "file3.txt"}


def test_scan_directory_exclusions(tmp_path: Path) -> None:
    """Verify that system dirs, root categories, .DS_Store and symlinks are excluded."""
    # Normal file
    (tmp_path / "normal.jpg").touch()

    # System directory
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").touch()

    # Category directory at root
    images_dir = tmp_path / "Images"
    images_dir.mkdir()
    (images_dir / "already_done.jpg").touch()

    # Category directory in subdirectory (should NOT be excluded even at root,
    # wait: category directory is excluded only at the root level of target)
    sub = tmp_path / "subdir"
    sub.mkdir()
    sub_images_dir = sub / "Images"
    sub_images_dir.mkdir()
    (sub_images_dir / "nested_done.jpg").touch()

    # .DS_Store file
    (tmp_path / ".DS_Store").touch()

    # Symlink file (should be ignored)
    target = tmp_path / "normal.jpg"
    link = tmp_path / "link.jpg"
    with suppress(OSError):
        link.symlink_to(target)

    # 1. Non-recursive scan
    files_non_rec = scan_directory(tmp_path, recursive=False)
    names_non_rec = {f.name for f in files_non_rec}
    assert "config" not in names_non_rec
    assert "already_done.jpg" not in names_non_rec
    assert ".DS_Store" not in names_non_rec
    assert "link.jpg" not in names_non_rec
    assert names_non_rec == {"normal.jpg"}

    # 2. Recursive scan
    files_rec = scan_directory(tmp_path, recursive=True)
    names_rec = {f.name for f in files_rec}
    assert "config" not in names_rec  # Excluded system dir
    assert "already_done.jpg" not in names_rec  # Excluded category dir at root
    assert "nested_done.jpg" in names_rec  # NOT excluded because nested
    assert "link.jpg" not in names_rec  # Excluded symlink
    assert ".DS_Store" not in names_rec
