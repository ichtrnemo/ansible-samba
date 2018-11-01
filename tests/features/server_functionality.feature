@controllers
Feature: Domain controllers

  @connectivity
  Scenario: Each domain controller can see each other
    Given From any domain controller
    When I ping other controllers
    Then They reply to ping request

  @users
  Scenario: Users list
    Given From any domain controller
    When I try to get users list
    Then It returns non empty list that contains Administrator user
