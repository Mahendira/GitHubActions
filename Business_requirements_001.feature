Feature: Business requirement 001

  Scenario: Business requirement 001
    Given the requirement file "Business_requirements_001.txt" is available
    And the business need is clearly described
    """
      The system should allow a user to perform a search query on the repository or box or drop box contains images using metadata details.
    """
    When the requirement is reviewed by the business owner
    Then a matching Cucumber feature file should be created with a valid Given/When/Then flow
