"""Tests for the CLI module."""

from pathlib import Path

from typer.testing import CliRunner

from autofileorganizer.cli import app

runner = CliRunner()


def test_cli_version() -> None:
    """Verify CLI version option prints version and exits."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "AutoFileOrganizer version" in result.stdout


def test_cli_help() -> None:
    """Verify CLI help option prints usage information."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Organize files in the target directory" in result.stdout


def test_cli_organize_defaults(tmp_path: Path, monkeypatch: Path) -> None:
    """Verify CLI organizing default folder runs successfully."""
    # Create a test file
    (tmp_path / "photo.jpg").touch()

    # Change current working directory to tmp_path so it organizes Path.cwd()
    monkeypatch.chdir(tmp_path)

    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert "ORGANIZATION COMPLETE" in result.stdout
    assert "photo.jpg" in result.stdout
    assert (tmp_path / "Images" / "photo.jpg").exists()


def test_cli_organize_specific_path(tmp_path: Path) -> None:
    """Verify CLI organizing a specific target path runs successfully."""
    # Create target and test file
    target = tmp_path / "target_folder"
    target.mkdir()
    (target / "doc.pdf").touch()

    result = runner.invoke(app, [str(target)])
    assert result.exit_code == 0
    assert "ORGANIZATION COMPLETE" in result.stdout
    assert "doc.pdf" in result.stdout
    assert (target / "Documents" / "doc.pdf").exists()


def test_cli_organize_dry_run(tmp_path: Path) -> None:
    """Verify CLI dry-run option prevents files from being moved."""
    (tmp_path / "song.mp3").touch()

    result = runner.invoke(app, [str(tmp_path), "--dry-run"])
    assert result.exit_code == 0
    assert "SIMULATION MODE" in result.stdout
    assert "song.mp3" in result.stdout
    assert (tmp_path / "song.mp3").exists()
    assert not (tmp_path / "Music" / "song.mp3").exists()


def test_cli_organize_recursive(tmp_path: Path) -> None:
    """Verify CLI recursive option processes subfolders."""
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "archive.zip").touch()

    # 1. Run without recursive (should not move)
    result_non_rec = runner.invoke(app, [str(tmp_path)])
    assert result_non_rec.exit_code == 0
    assert "archive.zip" not in result_non_rec.stdout
    assert (sub / "archive.zip").exists()

    # 2. Run with recursive
    result_rec = runner.invoke(app, [str(tmp_path), "--recursive"])
    assert result_rec.exit_code == 0
    assert "archive.zip" in result_rec.stdout
    assert not (sub / "archive.zip").exists()
    assert (tmp_path / "Archives" / "archive.zip").exists()
