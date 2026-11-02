#!/usr/bin/env python3
"""Unit tests for obsidian-to-hugo.py."""

import importlib.util
import tempfile
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

    def test_description_from_obsidian_top_level_for_posts(self):
        """A top-level 'description' field is copied to the post."""
        note = {
            "title": "Test Post",
            "description": "A description from Obsidian.",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "test-post"
        )

        self.assertEqual(frontmatter["description"], "A description from Obsidian.")

    def test_description_falls_back_to_metadata(self):
        """A 'description' property under metadata is used when top-level is absent."""
        note = {
            "title": "Test Post",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
                "description": "A metadata description.",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "test-post"
        )

        self.assertEqual(frontmatter["description"], "A metadata description.")

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

    def test_description_from_obsidian_top_level_for_books(self):
        """A top-level 'description' field is copied to books."""
        note = {
            "title": "Test Book",
            "description": "A book description from Obsidian.",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["book"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "books", self.books_archetype, note, "test-book"
        )

        self.assertEqual(
            frontmatter["description"], "A book description from Obsidian."
        )

    def test_post_title_split_on_dash_moves_suffix_to_description(self):
        """For posts, text after the first dash in the title becomes description."""
        note = {
            "title": "AI Today 16 - Intelligence is not thinking",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "ai-today-16"
        )

        self.assertEqual(frontmatter["title"], "AI Today 16")
        self.assertEqual(
            frontmatter["description"], "Intelligence is not thinking"
        )

    def test_explicit_description_overrides_title_suffix(self):
        """An explicit description field takes precedence over title-derived description."""
        note = {
            "title": "AI Today 16 - Intelligence is not thinking",
            "description": "Explicit description.",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["post"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "posts", self.posts_archetype, note, "ai-today-16"
        )

        self.assertEqual(frontmatter["description"], "Explicit description.")

    def test_book_titles_are_not_split_on_dash(self):
        """Book titles keep dashes intact."""
        note = {
            "title": "Some Book - A subtitle",
            "created": "2024-01-15T10:30:00Z",
            "tags": ["book"],
            "metadata": {
                "date created": "Monday, January 15th 2024, 10:30:00 am",
            },
        }

        frontmatter = obsidian_to_hugo.build_frontmatter(
            "books", self.books_archetype, note, "some-book"
        )

        self.assertEqual(frontmatter["title"], "Some Book - A subtitle")


class TestFindStaleFiles(unittest.TestCase):
    """Tests for find_stale_files."""

    def setUp(self):
        """Create a temporary content directory."""
        self.content_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        """Remove the temporary content directory."""
        for path in self.content_dir.iterdir():
            path.unlink()
        self.content_dir.rmdir()

    def test_default_keeps_unrelated_stale_files(self):
        """By default, files that are not duplicates are preserved."""
        expected = self.content_dir / "expected.md"
        stale = self.content_dir / "stale.md"
        expected.write_text("---\nfoo\n---\n\nexpected")
        stale.write_text("---\nfoo\n---\n\nstale")

        result = obsidian_to_hugo.find_stale_files(
            self.content_dir, {expected}, {expected: "expected"}
        )

        self.assertEqual(result, [])

    def test_default_removes_prefixed_duplicates(self):
        """Files prefixed with the old directory slug are removed as duplicates."""
        expected = self.content_dir / "expected.md"
        duplicate = self.content_dir / "personal-www-posts-expected.md"
        expected.write_text("---\nfoo\n---\n\nexpected")
        duplicate.write_text("---\nfoo\n---\n\nduplicate")

        result = obsidian_to_hugo.find_stale_files(
            self.content_dir, {expected}, {expected: "expected"}
        )

        self.assertEqual(result, [duplicate])

    def test_default_removes_body_duplicates(self):
        """Files with the same body as a generated file are removed as duplicates."""
        expected = self.content_dir / "expected.md"
        duplicate = self.content_dir / "old-expected.md"
        expected.write_text("---\nfoo\n---\n\nshared body")
        duplicate.write_text("---\nbar\n---\n\nshared body")

        result = obsidian_to_hugo.find_stale_files(
            self.content_dir, {expected}, {expected: "shared body"}
        )

        self.assertEqual(result, [duplicate])

    def test_default_keeps_prefixed_files_without_expected_match(self):
        """Prefixed files that do not shadow an expected file are preserved."""
        prefixed = self.content_dir / "personal-www-posts-unique.md"
        prefixed.write_text("---\nfoo\n---\n\nunique")

        result = obsidian_to_hugo.find_stale_files(self.content_dir, set(), {})

        self.assertEqual(result, [])

    def test_clean_removes_all_unexpected_files(self):
        """With clean=True, all files not in the expected set are flagged."""
        expected = self.content_dir / "expected.md"
        stale = self.content_dir / "stale.md"
        expected.write_text("---\nfoo\n---\n\nexpected")
        stale.write_text("---\nfoo\n---\n\nstale")

        result = obsidian_to_hugo.find_stale_files(
            self.content_dir, {expected}, {expected: "expected"}, clean=True
        )

        self.assertEqual(result, [stale])

    def test_skips_hugo_reserved_files(self):
        """Files starting with an underscore are never flagged as stale."""
        index = self.content_dir / "_index.md"
        index.write_text("index")

        result = obsidian_to_hugo.find_stale_files(self.content_dir, set(), {})

        self.assertEqual(result, [])

    def test_returns_empty_when_all_files_expected(self):
        """An empty list is returned when every file is expected."""
        expected = self.content_dir / "expected.md"
        expected.write_text("---\nfoo\n---\n\nexpected")

        result = obsidian_to_hugo.find_stale_files(
            self.content_dir, {expected}, {expected: "expected"}
        )

        self.assertEqual(result, [])


if __name__ == "__main__":
    unittest.main()
