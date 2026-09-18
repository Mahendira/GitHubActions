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
