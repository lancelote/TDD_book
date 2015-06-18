Feature: Lists Web App
  App should provide minimum to-do list interface

  Scenario: Simple visit
    When I open an index page
    Then I see a title says "To-Do"
#    And I am invited to enter "To-DO" item
#    Then I enter "Buy peacock feathers" into a text box
#    When I hit enter
#    Then Page updates and now it lists "1: Buy peacock feathers"
#    And There is still a text box inviting me to enter another To-Do item
#    Then I enter "Use peacock feathers to make a fly" into a text box
#    When I hit enter
#    Then Page updates and now it lists "1: Buy peacock feathers\nUse peacock feathers to make a fly"
#    And I see the site has generated a unique url for me
#    And There is a explanatory text about it
#    When I visit this url
#    Then I see my To-Do list
