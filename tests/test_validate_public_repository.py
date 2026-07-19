"""Regression tests for public wording validation."""

from __future__ import annotations

import unittest

from scripts import validate_public_repository as validator


class PublicWordingTests(unittest.TestCase):
    def test_allows_legitimate_public_research_language(self) -> None:
        allowed = (
            "Research and portfolio demonstration.",
            "The recorded workflow is retained for reproducibility.",
            "Results use an experimental held-out set.",
            "Access is controlled by the dataset provider.",
            "Methodological limitations are documented.",
            "Metrics were not recomputed during repository preparation.",
            "This academic project documents public research methods.",
        )

        for text in allowed:
            with self.subTest(text=text):
                self.assertEqual(validator.check_public_wording("README.md", text), [])

    def test_rejects_specific_private_or_submission_language(self) -> None:
        disallowed = (
            "Send the draft to my private supervisor.",
            "This is a coursework submission.",
            "Attach this university module submission.",
            "See the confidential local report.",
            "Copy unpublished institutional material here.",
            "The files are still in private preparation.",
        )

        for text in disallowed:
            with self.subTest(text=text):
                errors = validator.check_public_wording("README.md", text)
                self.assertEqual(len(errors), 1)
                self.assertIn("README.md:1", errors[0])

    def test_reports_each_match_with_its_line_number(self) -> None:
        text = "Public introduction.\nConfidential local report.\nCoursework submission.\n"

        errors = validator.check_public_wording("notes.md", text)

        self.assertEqual(len(errors), 2)
        self.assertTrue(any("notes.md:2" in error for error in errors))
        self.assertTrue(any("notes.md:3" in error for error in errors))

    def test_rejects_private_absolute_paths(self) -> None:
        examples = (
            "/Users/researcher/Desktop/private.csv",
            r"C:\Users\researcher\Desktop\private.csv",
        )

        for text in examples:
            with self.subTest(text=text):
                errors = validator.check_public_wording("notes.md", text)
                self.assertEqual(len(errors), 1)
                self.assertIn("Personal absolute path", errors[0])


if __name__ == "__main__":
    unittest.main()
