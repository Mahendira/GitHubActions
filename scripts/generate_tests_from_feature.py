#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip())
    normalized = normalized.strip("_")
    return normalized.lower() or "feature"


def parse_feature_file(feature_path: str | Path) -> dict:
    path = Path(feature_path)
    content = path.read_text(encoding="utf-8")

    feature_match = re.search(r"^Feature:\s*(.+)$", content, flags=re.MULTILINE)
    if not feature_match:
        raise ValueError(f"No Feature declaration found in {path}")

    feature_name = feature_match.group(1).strip()

    scenario_match = re.search(r"^\s*Scenario:\s*(.+)$", content, flags=re.MULTILINE)
    scenario_name = scenario_match.group(1).strip() if scenario_match else "Generated scenario"

    steps = []
    for line in content.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("Feature:") or stripped.startswith("Scenario:"):
            continue
        if re.match(r"^(Given|When|Then|And|But)\b", stripped):
            steps.append(stripped)

    return {
        "feature_name": feature_name,
        "scenario_name": scenario_name,
        "steps": steps,
    }


def generate_unittest_file(feature: dict) -> str:
    class_name = "Test" + "".join(part.capitalize() for part in feature["feature_name"].split())
    scenario_slug = slugify(feature["scenario_name"])
    if not class_name:
        class_name = "TestGeneratedFeature"

    lines = [
        "import unittest",
        "",
        f"class {class_name}(unittest.TestCase):",
        "",
        f"    def test_{scenario_slug}(self):",
        "        # Generated from feature scenario: {}".format(feature["scenario_name"]),
        "        self.assertTrue(True)",
        "",
    ]
    return "\n".join(lines) + "\n"


def generate_step_definition_file(feature: dict) -> str:
    feature_slug = slugify(feature["feature_name"])
    step_lines = []
    for step in feature["steps"]:
        keyword, _, remainder = step.partition(" ")
        normalized = remainder.strip()
        if not normalized:
            continue
        decorator = {
            "Given": "given",
            "When": "when",
            "Then": "then",
            "And": "given",
            "But": "given",
        }.get(keyword, "given")
        step_lines.append(f"@{decorator}('{normalized}')")
        step_lines.append("def step_impl(context):")
        step_lines.append("    assert context is not None")
        step_lines.append("")

    file_lines = [
        "from behave import given, then, when",
        "",
        "",
        f"# Auto-generated step definitions for {feature['feature_name']}",
        "",
    ]
    file_lines.extend(step_lines)
    if not step_lines:
        file_lines.extend([
            "@given('a generated step')",
            "def step_impl(context):",
            "    assert context is not None",
            "",
        ])
    return "\n".join(file_lines) + "\n"


def generate_files_from_feature(feature_path: str | Path) -> tuple[Path, Path]:
    feature = parse_feature_file(feature_path)
    feature_path = Path(feature_path)
    base_name = slugify(feature["feature_name"])
    test_dir = feature_path.parent / "tests"
    if not test_dir.exists():
        test_dir.mkdir(parents=True, exist_ok=True)
    step_dir = feature_path.parent / "features" / "steps"
    if not step_dir.exists():
        step_dir.mkdir(parents=True, exist_ok=True)

    unit_test_path = test_dir / f"test_{base_name}.py"
    unit_test_path.write_text(generate_unittest_file(feature), encoding="utf-8")

    step_file_path = step_dir / f"{base_name}_steps.py"
    step_file_path.write_text(generate_step_definition_file(feature), encoding="utf-8")
    return unit_test_path, step_file_path


def find_feature_files(paths):
    if paths:
        result = []
        for raw_path in paths:
            path = Path(raw_path)
            if path.is_dir():
                result.extend(sorted(path.rglob("*.feature")))
            elif path.exists() and path.suffix.lower() == ".feature":
                result.append(path)
            else:
                raise SystemExit(f"No matching feature file was found: {raw_path}")
        return result
    return sorted(Path(".").rglob("*.feature"))


def main():
    parser = argparse.ArgumentParser(description="Generate unit tests and Cucumber step definitions from feature files.")
    parser.add_argument("paths", nargs="*", help="Path or glob to .feature file(s)")
    args = parser.parse_args()

    feature_files = find_feature_files(args.paths)
    if not feature_files:
        print("No .feature files were found.")
        return 0

    for feature_file in feature_files:
        unit_test_path, step_file_path = generate_files_from_feature(feature_file)
        print(f"Generated: {unit_test_path}")
        print(f"Generated: {step_file_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
