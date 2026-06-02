"""Directory scanning logic.

This module is responsible for discovering all files in a target directory
while applying exclusion rules for system folders, category directories,
and dangerous symlinks.
"""

from pathlib import Path

from autofileorganizer.categories import CATEGORY_FOLDERS

# System folders to exclude from scanning
EXCLUDED_SYSTEM_DIRS: set[str] = {
    ".git",
    ".github",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "node_modules",
}


def scan_directory(target_path: Path, recursive: bool = False) -> list[Path]:
    """Scan a target directory and return a list of files to organize.

    Excludes:
    - System directories (e.g., .git, __pycache__).
    - Output category directories at the root of the target directory
      (Images, Videos, etc.) to prevent infinite loops or reorganizing.
    - Dangerous symbolic links.
    - Non-file entries (directories, sockets, devices).

    Args:
        target_path: Path to the target directory to scan.
        recursive: Whether to scan subdirectories.

    Returns:
        List of Path objects representing files to be organized.
    """
    files_to_organize: list[Path] = []

    # Category folder names to exclude at the root of target_path
    excluded_category_dirs: set[str] = set(CATEGORY_FOLDERS.values())

    if not target_path.exists() or not target_path.is_dir():
        return []

    # Helper function to walk the directory structure
    def _walk(current_dir: Path, is_root: bool) -> None:
        try:
            for entry in current_dir.iterdir():
                # Safety checks
                # Exclude symlinks to prevent dangerous behaviors
                if entry.is_symlink():
                    continue

                if entry.is_dir():
                    # Exclude system dirs anywhere in the tree
                    if entry.name in EXCLUDED_SYSTEM_DIRS:
                        continue

                    # Exclude category folders only at the root level of target
                    if is_root and entry.name in excluded_category_dirs:
                        continue

                    if recursive:
                        _walk(entry, is_root=False)
                elif entry.is_file():
                    # Ignore .DS_Store file itself
                    if entry.name == ".DS_Store":
                        continue
                    files_to_organize.append(entry)
        except PermissionError:
            # Silently skip directories where we don't have access
            pass

    _walk(target_path, is_root=True)
    return files_to_organize
