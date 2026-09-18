import os
import tempfile
import unittest
from pathlib import Path

from scripts.generate_feature_from_requirement import build_openai_prompt, generate_feature_file


class GenerateFeatureTests(unittest.TestCase):
    def test_build_openai_prompt_contains_requirement_and_gherkin_guidance(self):
        prompt = build_openai_prompt(
            "Business_requirements_001.txt",
            "The system should allow customers to place orders.",
        )
        self.assertIn("Business_requirements_001.txt", prompt)
        self.assertIn("Given", prompt)
        self.assertIn("When", prompt)
        self.assertIn("Then", prompt)
        self.assertIn("Gherkin", prompt)

    def test_generate_feature_file_writes_explicit_content(self):
        requirement_text = "A user can create an order."
        with tempfile.TemporaryDirectory() as tmp_dir:
            requirement_path = Path(tmp_dir) / "Business_requirements_002.txt"
            requirement_path.write_text(requirement_text, encoding="utf-8")

            generated_path = generate_feature_file(requirement_path, feature_text="Feature: Example\n\nScenario: Example\n  Given ...\n  When ...\n  Then ...\n")

            self.assertTrue(generated_path.exists())
            self.assertIn("Feature: Example", generated_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
