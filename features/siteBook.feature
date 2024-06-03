Feature: My Site Book

  Scenario: Verify My Site Book
    Given User navigate to the my site book URL
    Then User verify the title should be the configured title
    When User click on login button
    Then User navigate to the login page
    When User enter mobile number
    When User enter password
    Then User navigate to the projects page
    When User verify sample project cards visible
    Then User selects the sample project card 
    When User selects Detailed Estimate from list
    Then User verify details of the rows

    Scenario: Verify My Site Book with wrong data
    Given User navigate to the my site book URL
    Then User verify the title should be the configured title
    When User click on login button
    Then User navigate to the login page
    When User enter mobile number
    When User enter password
    Then User navigate to the projects page
    When User verify sample project cards visible
    Then User selects the sample project card 
    When User selects Detailed Estimate from list
    Then User verify details of the rows with wrong data

