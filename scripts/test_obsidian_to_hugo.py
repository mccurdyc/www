#!/usr/bin/env python3
"""Unit tests for obsidian-to-hugo.py."""

import importlib.util
import unittest
from pathlib import Path

# Load obsidian-to-hugo.py as a module despite the hyphen in its filename.
spec = importlib.util.spec_from_file_location(
    "obsidian_to_hugo",
    str(Path(__file__).parent / "obsidian-to-hugo.py"),
)
obsidian_to_hugo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(obsidian_to_hugo)


class TestBuildFrontmatter(unittest.TestCase):
    """Tests for build_frontmatter."""

    def setUp(self):
        """Set up paths used by each test."""
        self.archetypes_dir = obsidian_to_hugo.ARCHETYPES_DIR
        self.posts_archetype = self.archetypes_dir / "posts.md"
        self.books_archetype = self.archetypes_dir / "books.md"

    def test_description_from_obsidian_metadata_for_posts(self):
        """A 'description' property in Obsidian frontmatter is copied to the post."""
        note = {
            "title": "Test Post",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
                "description": "A description from Obsidian.",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "test-post"
        )

        self.assertEqual(frontmatter["description"], "A description from Obsidian.")

    def test_description_defaults_to_archetype_when_missing(self):
        """When Obsidian has no description, the archetype default is kept."""
        note = {
            "title": "Test Post",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "test-post"
        )

        self.assertEqual(frontmatter["description"], "")

    def test_description_from_obsidian_metadata_for_books(self):
        """A 'description' property in Obsidian frontmatter is copied to books."""
        note = {
            "title": "Test Book",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["book"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
                "description": "A book description from Obsidian.",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "books", self.books_archetype, note, "test-book"
        )

        self.assertEqual(
            frontmatter["description"], "A book description from Obsidian."
        )


if __name__ == "__main__":
    unittest.main()
