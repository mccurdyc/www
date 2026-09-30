#!/usr/bin/env python3
"""Unit tests for photo-post.py."""

import importlib.util
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

# Load photo-post.py as a module despite the hyphen in its filename.
_spec = importlib.util.spec_from_file_location(
    "photo_post",
    str(Path(__file__).parent / "photo-post.py"),
)
photo_post = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(photo_post)


class TestListImages(unittest.TestCase):
    """Tests for list_images."""

    @patch.object(photo_post, "run")
    def test_filters_directory_entry(self, mock_run):
        """Directory URLs returned by gsutil ls are not emitted as images."""
        mock_run.return_value = MagicMock(
            stdout=(
                "gs://images.mccurdyc.dev/images/2026/09/30/roll/WALK-WITH-BANKSY/\n"
                "gs://images.mccurdyc.dev/images/2026/09/30/roll/WALK-WITH-BANKSY/1.jpeg\n"
                "gs://images.mccurdyc.dev/images/2026/09/30/roll/WALK-WITH-BANKSY/2.jpeg\n"
            ),
        )

        images = photo_post.list_images("2026/09/30/roll/WALK-WITH-BANKSY")

        self.assertEqual(len(images), 2)
        self.assertTrue(
            all(not url.endswith("/") for url in images),
            msg="directory URL should be filtered out",
        )

    @patch.object(photo_post, "run")
    def test_natural_sort_order(self, mock_run):
        """Filenames sort numerically (1, 2, 10) instead of lexicographically."""
        mock_run.return_value = MagicMock(
            stdout=(
                "gs://images.mccurdyc.dev/images/2026/early/\n"
                "gs://images.mccurdyc.dev/images/2026/early/10.jpeg\n"
                "gs://images.mccurdyc.dev/images/2026/early/1.jpeg\n"
                "gs://images.mccurdyc.dev/images/2026/early/2.jpeg\n"
                "gs://images.mccurdyc.dev/images/2026/early/11.jpeg\n"
            ),
        )

        images = photo_post.list_images("2026/early")
        basenames = [Path(url).name for url in images]

        self.assertEqual(basenames, ["1.jpeg", "2.jpeg", "10.jpeg", "11.jpeg"])


class TestImagePathFromGcs(unittest.TestCase):
    """Tests for image_path_from_gcs."""

    def test_strips_gcs_base(self):
        """A gs:// URL is converted to a site-relative /images/... path."""
        gcs_url = "gs://images.mccurdyc.dev/images/2026/early/0001.jpg"
        self.assertEqual(
            photo_post.image_path_from_gcs(gcs_url),
            "/images/2026/early/0001.jpg",
        )

    def test_passes_through_non_gcs_url(self):
        """Non-GCS URLs are returned unchanged."""
        url = "/images/2026/early/0001.jpg"
        self.assertEqual(photo_post.image_path_from_gcs(url), url)


if __name__ == "__main__":
    unittest.main()
