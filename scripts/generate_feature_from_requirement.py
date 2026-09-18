#!/usr/bin/env python3
import argparse
import json
import os
import re
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


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

    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")

        print(f"OpenAI HTTP status: {exc.code}")
        print(f"OpenAI error response: {error_body}")

        raise RuntimeError(
            f"OpenAI API returned HTTP {exc.code}: {error_body}"
        ) from exc

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


def find_git_auth_token() -> str | None:
    for env_name in ("GITHUB_TOKEN", "GH_TOKEN", "GIT_TOKEN"):
        token = os.getenv(env_name)
        if token and token.strip():
            return token.strip()
    return None


def inject_git_auth_token(raw_target: str) -> str:
    if not raw_target.startswith(("http://", "https://")):
        return raw_target

    parsed = urlparse(raw_target)
    hostname = (parsed.hostname or "").lower()
    if not hostname or "@" in (parsed.netloc or ""):
        return raw_target
    if hostname != "github.com" and not hostname.endswith(".github.com"):
        return raw_target

    token = find_git_auth_token()
    if not token:
        return raw_target

    credentials = f"x-access-token:{token}"
    netloc = parsed.hostname
    if parsed.port:
        netloc = f"{netloc}:{parsed.port}"
    return parsed._replace(netloc=f"{credentials}@{netloc}").geturl()


def resolve_repo_target(repo_target: str | Path, base_dir: Path | None = None) -> Path:
    raw_target = str(repo_target).strip() if repo_target is not None else "."
    if not raw_target:
        raw_target = "."

    if raw_target.startswith(("http://", "https://", "git@", "ssh://", "git://", "file://")):
        parsed = urlparse(raw_target)
        repo_name = parsed.path.rstrip("/").rsplit("/", 1)[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]
        if not repo_name:
            repo_name = "cloned-repo"

        clone_dir = (base_dir or Path.cwd()) / "cloned-repos" / repo_name
        if not clone_dir.exists():
            clone_dir.parent.mkdir(parents=True, exist_ok=True)
            git_clone_target = inject_git_auth_token(raw_target)
            subprocess.run(["git", "clone", "--depth", "1", git_clone_target, str(clone_dir)], check=True, capture_output=True, text=True)
        return clone_dir

    target_path = Path(raw_target).expanduser()
    if not target_path.is_absolute():
        target_path = (base_dir or Path.cwd()) / target_path
    return target_path.resolve()


def update_readme_recent_changes(readme_path: Path, requirement_file_name: str, feature_file_name: str) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    summary = (
        f"- {timestamp}: Generated {feature_file_name} from {requirement_file_name}."
    )

    if readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")
    else:
        content = "# Repository\n\n"

    if "## Recent changes" in content:
        recent_section = content.split("## Recent changes", 1)[1]
        if summary in recent_section:
            return readme_path
        updated = content.rstrip() + "\n\n" + summary + "\n"
    else:
        updated = content.rstrip() + "\n\n## Recent changes\n\n" + summary + "\n"

    readme_path.write_text(updated.rstrip() + "\n", encoding="utf-8")
    return readme_path


def ensure_target_repo(
    repo_path: Path | str,
    requirement_text: str,
    requirement_name: str | None = None,
    feature_text: str | None = None,
) -> Path:
    repo_path = resolve_repo_target(repo_path)
    repo_path.mkdir(parents=True, exist_ok=True)

    if requirement_name is None:
        requirement_name = "Business_requirements_001"
    requirement_name = requirement_name.rstrip(".txt")
    requirement_path = repo_path / f"{requirement_name}.txt"
    requirement_path.write_text(requirement_text.strip() + "\n", encoding="utf-8")

    readme_path = repo_path / "README.md"
    if not readme_path.exists():
        readme_path.write_text(
            "# Repository\n\nThis repository was created automatically for feature generation.\n",
            encoding="utf-8",
        )

    generated_path = generate_feature_file(requirement_path, feature_text=feature_text)
    update_readme_recent_changes(readme_path, requirement_path.name, generated_path.name)
    return generated_path


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
    parser.add_argument("--repo-target", dest="repo_target", help="Local repo path or GitHub repo URL to create/update and generate the feature file in.")
    parser.add_argument("--repo-path", dest="repo_path", help="Backward-compatible alias for --repo-target.")
    parser.add_argument("--requirement-text", dest="requirement_text", help="Requirement text to use when creating a feature in a target repo.")
    parser.add_argument("--requirement-name", dest="requirement_name", help="Base requirement filename without extension, e.g. Business_requirements_001.")
    args = parser.parse_args()

    repo_target = args.repo_target or args.repo_path
    if repo_target:
        if not args.requirement_text:
            raise SystemExit("--requirement-text is required when --repo-target is provided.")
        generated_path = ensure_target_repo(repo_target, args.requirement_text, args.requirement_name)
        print(f"Repo created/updated at: {generated_path.parent}")
        print(f"Generated: {generated_path}")
        return 0

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
