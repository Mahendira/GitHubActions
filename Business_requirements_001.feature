Feature: Search API

  As an API consumer
  I want to search for resources using a REST API
  So that I can retrieve matching records using standard HTTP operations

  Background:
    Given the Search API is available at "/api/v1/search"
    And the API produces responses with content type "application/json"
    And the API is documented using OpenAPI 3.1

  Scenario: Search using a valid search query
    Given records exist that match the search term "cloud"
    When the client sends a GET request to "/api/v1/search?query=cloud"
    Then the API should return HTTP status 200
    And the response should contain matching search results
    And the response should conform to the SearchResponse OpenAPI schema

  Scenario: Search with pagination
    Given more than 10 records match the search term "AWS"
    When the client sends a GET request to "/api/v1/search?query=AWS&page=0&size=10"
    Then the API should return HTTP status 200
    And the response should contain at most 10 results
    And the response should contain pagination metadata
    And the response should contain the current page
    And the response should contain the total number of results

  Scenario: Search with no matching results
    Given no records match the search term "nonexistent-value"
    When the client sends a GET request to "/api/v1/search?query=nonexistent-value"
    Then the API should return HTTP status 200
    And the response should contain an empty results array
    And the total number of results should be 0

  Scenario: Search without the required query parameter
    Given the "query" parameter is required
    When the client sends a GET request to "/api/v1/search"
    Then the API should return HTTP status 400
    And the response should contain an error code
    And the response should contain an error message
    And the error response should conform to the ErrorResponse OpenAPI schema

  Scenario: Search with an invalid page size
    Given the maximum allowed page size is 100
    When the client sends a GET request to "/api/v1/search?query=cloud&size=500"
    Then the API should return HTTP status 400
    And the response should indicate that the "size" parameter is invalid

  Scenario: Search API returns an unexpected server error
    Given an unexpected error occurs while processing the search request
    When the client sends a GET request to "/api/v1/search?query=cloud"
    Then the API should return HTTP status 500
    And the response should contain a standard error response
    And the response should conform to the ErrorResponse OpenAPI schema

  Scenario: Search API follows the OpenAPI contract
    Given the Search API has an OpenAPI specification
    When the OpenAPI specification is validated
    Then the specification should define the "/api/v1/search" path
    And the path should define a GET operation
    And the GET operation should define the "query" parameter
    And the GET operation should define the "page" parameter
    And the GET operation should define the "size" parameter
    And the GET operation should define HTTP 200 responses
    And the GET operation should define HTTP 400 responses
    And the GET operation should define HTTP 500 responses
    And all request parameters should have schemas
    And all response bodies should have schemas