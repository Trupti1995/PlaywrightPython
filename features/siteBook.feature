Feature: My Site Book

Background: Open and check title
    Given User navigate to the my site book URL
    Then User verify the title should be the configured title

  Scenario: Login to my site book
    When User click on login button
    Then User navigate to the login page
    When User enter mobile number
    When User enter password
    Then User navigate to the projects page