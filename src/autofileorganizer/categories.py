"""File categorization configuration and detection logic.

This module maps file extensions to predefined categories and associated
Unicode icons according to the design system.
"""


# Mapping of category names to their display icons (from design.md)
CATEGORY_ICONS: dict[str, str] = {
    "Images": "📷",
    "Videos": "🎥",
    "Documents": "📄",
    "Music": "🎵",
    "Archives": "📦",
    "Code": "💻",
    "Others": "📁",
}

# The plan.md specifies creating folders: Images/, Videos/,
# Documents/, Music/, Archives/, Code/, Others/.
# We'll use the exact casing and spelling from plan.md.
CATEGORY_FOLDERS: dict[str, str] = {
    "Images": "Images",
    "Videos": "Videos",
    "Documents": "Documents",
    "Music": "Music",
    "Archives": "Archives",
    "Code": "Code",
    "Others": "Others",
}

# Extension mappings (case-insensitive, without leading dot)
EXTENSION_MAP: dict[str, set[str]] = {
    "Images": {"jpg", "jpeg", "png", "gif", "webp", "svg"},
    "Videos": {"mp4", "mov", "avi", "mkv"},
    "Documents": {"pdf", "docx", "doc", "xlsx", "pptx", "txt"},
    "Music": {"mp3", "wav", "flac"},
    "Archives": {"zip", "rar", "7z", "tar", "gz"},
    "Code": {
        "py",
        "js",
        "ts",
        "jsx",
        "tsx",
        "html",
        "css",
        "java",
        "cpp",
        "c",
        "go",
        "rs",
    },
}


def get_category_for_extension(extension: str) -> str:
    """Return the category name for a given file extension.

    The check is case-insensitive. If no matching category is found,
    it returns 'Others'.

    Args:
        extension: The file extension (e.g., 'jpg', '.txt').

    Returns:
        The matched category name.
    """
    clean_ext = extension.lower().strip()
    if clean_ext.startswith("."):
        clean_ext = clean_ext[1:]

    for category, extensions in EXTENSION_MAP.items():
        if clean_ext in extensions:
            return category

    return "Others"
