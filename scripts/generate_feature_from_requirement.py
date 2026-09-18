#!/usr/bin/env python3
import argparse
import json
import os
import re
import urllib.request
from pathlib import Path


def read_requirement_text(file_path: Path) -> str:
    try:
        content = file_path.read_text(encoding="utf-8").strip()
        return content or "No requirement text was provided."
    except FileNotFoundError:
        raise SystemExit(f"File not found: {file_path}")


def slug_to_title(file_name: str) -> str:
    stem = Path(file_name).stem
    stem = stem.replace("Business_requirements_", "Business requirement ")
    stem = stem.replace("_", " ")
    return stem.strip()


def build_openai_prompt(file_name: str, requirement_text: str) -> str:
    return (
        "You are generating a valid Gherkin/Cucumber feature file.\n"
        f"Use this requirement file name: {file_name}\n\n"
        "Requirement text:\n"
        f"{requirement_text}\n\n"
        "Create a single .feature file with the following rules:\n"
        "- Output only valid Gherkin syntax\n"
        "- Start with a Feature declaration\n"
        "- Include exactly one Scenario with realistic Given/When/Then steps\n"
        "- No markdown fences, no commentary, no extra explanation\n"
        "- Ensure the text is easy to read and aligned to the business requirement\n"
    )


def call_openai_api(file_name: str, requirement_text: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set.")

    payload = {
        "model": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "messages": [
            {"role": "system", "content": "You generate valid Gherkin .feature files only."},
            {"role": "user", "content": build_openai_prompt(file_name, requirement_text)},
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        data = json.loads(response.read().decode("utf-8"))

    try:
        content = data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("Unexpected response format from OpenAI API.") from exc

    cleaned = re.sub(r"^```(?:gherkin)?\s*", "", content, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return cleaned.strip() + "\n"


def fallback_feature_text(requirement_path: Path, requirement_text: str) -> str:
    feature_title = slug_to_title(requirement_path.name)
    content_lines = [
        f"Feature: {feature_title}",
        "",
        f"  Scenario: {feature_title}",
        f'    Given the requirement file "{requirement_path.name}" is available',
        "    And the business need is clearly described",
        "    \"\"\"",
    ]

    for line in requirement_text.splitlines():
        content_lines.append(f"      {line if line else ''}")

    content_lines.extend([
        "    \"\"\"",
        "    When the requirement is reviewed by the business owner",
        "    Then a matching Cucumber feature file should be created with a valid Given/When/Then flow",
        "",
    ])

    return "\n".join(content_lines)


def generate_feature_file(requirement_path: Path, feature_text: str | None = None) -> Path:
    requirement_text = read_requirement_text(requirement_path)
    feature_path = requirement_path.with_suffix(".feature")

    if feature_text is not None:
        content = feature_text
    else:
        try:
            content = call_openai_api(requirement_path.name, requirement_text)
        except Exception as exc:
            print(f"OpenAI generation unavailable, using fallback template. Reason: {exc}")
            content = fallback_feature_text(requirement_path, requirement_text)

    feature_path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return feature_path


def find_requirement_files(paths):
    if paths:
        result = []
        for raw_path in paths:
            path = Path(raw_path)
            if path.is_dir():
                result.extend(sorted(path.rglob("Business_requirements_*.txt")))
            elif path.exists() and path.name.startswith("Business_requirements_") and path.suffix.lower() == ".txt":
                result.append(path)
            else:
                raise SystemExit(f"No matching requirement file was found: {raw_path}")
        return result

    return sorted(Path(".").rglob("Business_requirements_*.txt"))


def main():
    parser = argparse.ArgumentParser(description="Generate Gherkin feature files from business requirement text files.")
    parser.add_argument("paths", nargs="*", help="Path or glob to Business_requirements_*.txt file(s)")
    args = parser.parse_args()

    requirement_files = find_requirement_files(args.paths)
    if not requirement_files:
        print("No Business_requirements_*.txt files were found.")
        return 0

    for requirement_file in requirement_files:
        generated_path = generate_feature_file(requirement_file)
        print(f"Generated: {generated_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
