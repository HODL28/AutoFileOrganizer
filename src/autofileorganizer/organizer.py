"""Core file organization logic.

This module orchestrates the scanning, categorization, name resolution,
and movement of files, supporting both dry-runs and actual file operations.
"""

import time
from dataclasses import dataclass, field
from pathlib import Path

from autofileorganizer.categories import (
    CATEGORY_FOLDERS,
    get_category_for_extension,
)
from autofileorganizer.scanner import scan_directory
from autofileorganizer.utils import resolve_name_conflict


@dataclass
class OrganizationReport:
    """Represents the results of an organization run."""

    target_dir: Path
    dry_run: bool
    total_scanned: int = 0
    # List of (source_path, destination_path, category)
    moved_files: list[tuple[Path, Path, str]] = field(default_factory=list)
    # List of (source_path, error_message)
    failed_files: list[tuple[Path, str]] = field(default_factory=list)
    execution_duration: float = 0.0

    @property
    def total_moved(self) -> int:
        """Return the number of files successfully moved."""
        return len(self.moved_files)

    @property
    def total_failed(self) -> int:
        """Return the number of files that failed to move."""
        return len(self.failed_files)


def organize_directory(
    target_dir: Path, recursive: bool = False, dry_run: bool = False
) -> OrganizationReport:
    """Organize all files in target_dir into category folders.

    Args:
        target_dir: The directory to organize.
        recursive: Whether to scan subdirectories.
        dry_run: If True, simulate actions without modifying the filesystem.

    Returns:
        An OrganizationReport object containing details of the operations.
    """
    start_time = time.perf_counter()
    report = OrganizationReport(target_dir=target_dir, dry_run=dry_run)

    # 1. Scan directory
    files_to_organize = scan_directory(target_dir, recursive=recursive)
    report.total_scanned = len(files_to_organize)

    # Set to track target paths planned in this run (prevents dry-run collisions)
    allocated_paths: set[Path] = set()

    # Pre-calculate category folders
    category_paths: dict[str, Path] = {}
    for cat_name, folder_name in CATEGORY_FOLDERS.items():
        category_paths[cat_name] = target_dir / folder_name

    # 2. Process files
    for file_path in files_to_organize:
        try:
            # Determine category
            category = get_category_for_extension(file_path.suffix)
            dest_dir = category_paths[category]

            # Resolve name conflict
            dest_path = resolve_name_conflict(
                dest_dir, file_path.name, allocated_paths
            )
            allocated_paths.add(dest_path)

            if dry_run:
                # In dry run, just record the proposed operation
                report.moved_files.append((file_path, dest_path, category))
            else:
                # Ensure destination directory exists
                dest_dir.mkdir(parents=True, exist_ok=True)

                # Move the file (using rename)
                file_path.rename(dest_path)
                report.moved_files.append((file_path, dest_path, category))

        except Exception as e:
            report.failed_files.append((file_path, str(e)))

    report.execution_duration = time.perf_counter() - start_time
    return report
