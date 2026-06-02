"""Utility functions for file organization.

This module provides support functions, such as resolving file naming
conflicts (e.g., appending _1, _2 to files that already exist in the
destination).
"""

from pathlib import Path
from typing import Optional


def resolve_name_conflict(
    dest_dir: Path, filename: str, allocated_paths: Optional[set[Path]] = None
) -> Path:
    """Resolve file name conflicts in a destination directory.

    If a file with the same name exists or is already allocated for movement
    in the current run, this function appends '_1', '_2', etc., to the file
    stem.

    Args:
        dest_dir: The directory where the file will be placed.
        filename: The original name of the file.
        allocated_paths: Optional set of paths already planned to be used
            during dry-run/execution.

    Returns:
        A Path object representing the conflict-resolved target path.
    """
    path_obj = Path(filename)
    stem = path_obj.stem
    suffix = path_obj.suffix

    # Initial target path
    target_path = dest_dir / filename

    # Check if target_path exists or is in allocated_paths
    def is_taken(path: Path) -> bool:
        if path.exists():
            return True
        return bool(allocated_paths and path in allocated_paths)

    if not is_taken(target_path):
        return target_path

    # Increment suffix until an available path is found
    counter = 1
    while True:
        new_filename = f"{stem}_{counter}{suffix}"
        target_path = dest_dir / new_filename
        if not is_taken(target_path):
            return target_path
        counter += 1
