Feature: Search for images using metadata

  Scenario: User performs a search query on the repository for images
    Given the user is on the image repository page
    When the user enters metadata details "sunset" in the search bar
    And the user clicks on the search button
    Then the system should display a list of images related to "sunset" from the repository
