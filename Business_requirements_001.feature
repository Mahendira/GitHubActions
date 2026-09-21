Feature: Search Capability for Image Repositories

  Scenario: User performs a search query across multiple repositories
    Given the user is authenticated with a valid token
    And the user has access to the internal repository and Dropbox
    When the user searches for images with the query "holiday" 
    And applies filters for file type "jpg" and upload date "last month"
    Then the system should return a list of images matching the query
    And the response should include metadata for each image
    And the response should include pagination details
    And the response should have a status code of 200 OK
