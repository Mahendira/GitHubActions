Feature: Image Search Functionality

  Scenario: User performs a search query using metadata details
    Given the user has access to the image repository
    And the user has valid metadata details for the search
    When the user submits a search query with the metadata details
    Then the system should return a list of images matching the metadata
    And the response code should be 200 as per OpenAPI specification
    When the user submits a search query with invalid metadata details
    Then the system should return a response code of 400 as per OpenAPI specification
    When the user submits a search query with no metadata details
    Then the system should return a response code of 422 as per OpenAPI specification
