# GitHubActions

This repository demonstrates how a requirement file such as `Business_requirements_001.txt` can trigger a GitHub Action that generates a Cucumber-style `.feature` file automatically.

## How it works

- Add a file such as `Business_requirements_001.txt`.
- The workflow listens for changes matching `**/Business_requirements_*.txt`.
- A Python script reads the requirement text and creates a matching `.feature` file beside it.
- The generated feature file contains a valid `Feature`, `Scenario`, `Given`, `When`, and `Then` block.

## Example

If you add:

`Business_requirements_001.txt`

then the workflow creates:

`Business_requirements_001.feature`

with content like:

```gherkin
Feature: Business requirement 001

  Scenario: Business requirement 001
    Given the requirement file "Business_requirements_001.txt" is available
    And the business need is clearly described
    """
      The system should allow a user to request a new order and review the order status before payment is confirmed.
    """
    When the requirement is reviewed by the business owner
    Then a matching Cucumber feature file should be created with a valid Given/When/Then flow
```

## Trigger

The workflow runs on:

- a push to `main` when a matching requirement file is added or changed
- manual trigger from the GitHub Actions UI with an optional file path

## Manual workflow inputs

When you run the workflow manually, the GitHub Actions popup includes example values so you can adjust them as needed:

- `github_repo_url`: default `https://github.com/Mahendira/testingactions.git`
- `repo_visibility`: default `private` (`private` or `public`)
- `requirement_name`: default `Business_requirements_001`
- `requirement_text`: sample value describing the business requirement

## Required GitHub token for GitHub repo operations

If the target repository does not exist yet, or if the repository is private and needs access, the workflow requires a PAT.

Create a repository secret named `GH_PAT` in GitHub:

- GitHub repo → Settings → Secrets and variables → Actions → New repository secret
- Name: `GH_PAT`
- Value: a Personal Access Token for the account that owns the repository

The token must have permission to create and access the target GitHub repository. If the token is missing, the workflow exits with a clear error explaining how to fix it.

Without `GH_PAT`, GitHub Actions may fail with `Resource not accessible by integration (createRepository)` when the workflow tries to create a repo or clone a private repo.
