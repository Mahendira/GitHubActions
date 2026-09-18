import os
import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.generate_feature_from_requirement import (
    build_openai_prompt,
    ensure_target_repo,
    generate_feature_file,
    resolve_repo_target,
)


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

    def test_ensure_target_repo_creates_readme_and_feature_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo_dir = Path(tmp_dir) / "target-repo"

            generated_path = ensure_target_repo(
                repo_dir,
                requirement_text="The system should allow a user to create an order.",
                requirement_name="Business_requirements_010",
                feature_text="Feature: Example\n\nScenario: Example\n  Given ...\n  When ...\n  Then ...\n",
            )

            self.assertTrue(repo_dir.exists())
            self.assertTrue((repo_dir / "README.md").exists())
            self.assertTrue(generated_path.exists())
            readme_text = (repo_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("Recent changes", readme_text)
            self.assertIn("Business_requirements_010", readme_text)

    def test_resolve_repo_target_clones_remote_repository(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            base_dir = Path(tmp_dir)
            source_repo = base_dir / "source-repo"
            source_repo.mkdir()
            subprocess.run(["git", "init", str(source_repo)], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(source_repo), "config", "user.name", "Test User"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(source_repo), "config", "user.email", "test@example.com"], check=True, capture_output=True)
            (source_repo / "README.md").write_text("# source repo\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(source_repo), "add", "README.md"], check=True, capture_output=True)
            subprocess.run(["git", "-C", str(source_repo), "commit", "-m", "initial commit"], check=True, capture_output=True)

            cloned_repo = resolve_repo_target(f"file://{source_repo}", base_dir=base_dir)

            self.assertTrue(cloned_repo.exists())
            self.assertTrue((cloned_repo / "README.md").exists())
            self.assertIn("source repo", (cloned_repo / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
