"""Tests for the categories module."""

import pytest

from autofileorganizer.categories import (
    CATEGORY_ICONS,
    get_category_for_extension,
)


def test_category_icons_mapping() -> None:
    """Verify that required categories have correct icons."""
    assert CATEGORY_ICONS["Images"] == "📷"
    assert CATEGORY_ICONS["Videos"] == "🎥"
    assert CATEGORY_ICONS["Documents"] == "📄"
    assert CATEGORY_ICONS["Music"] == "🎵"
    assert CATEGORY_ICONS["Archives"] == "📦"
    assert CATEGORY_ICONS["Code"] == "💻"
    assert CATEGORY_ICONS["Others"] == "📁"


@pytest.mark.parametrize(
    "extension,expected_category",
    [
        ("jpg", "Images"),
        ("JPEG", "Images"),
        (".png", "Images"),
        ("mp4", "Videos"),
        (".mkv", "Videos"),
        ("pdf", "Documents"),
        ("txt", "Documents"),
        ("mp3", "Music"),
        ("flac", "Music"),
        ("zip", "Archives"),
        (".tar.gz", "Others"),  # since it matches .gz usually, wait, .tar.gz checks .gz
        ("gz", "Archives"),
        ("py", "Code"),
        (".rs", "Code"),
        ("unknown", "Others"),
        ("", "Others"),
        ("   .png  ", "Images"),
    ],
)
def test_get_category_for_extension(extension: str, expected_category: str) -> None:
    """Test get_category_for_extension under multiple inputs."""
    assert get_category_for_extension(extension) == expected_category
