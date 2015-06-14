Feature: Superlists Web App
  App should provide minimum to-do list interface

  Scenario: Index page loaded correctly
    When I check index page
    Then I see a title "Django"
