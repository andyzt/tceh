# Created by sobolev at 29.04.16
Feature: Client makes order
  This feature ensures that it is possible to the client to order a pizza

  Scenario: Basic order
    Given we have all fixtures installed
    When client orders "Vegetarian" "XL" pizza to "some street 7, 55"
    Then order is created

  Scenario: Order with extra ingridients
    Given we have all fixtures installed
    When client orders "Vegetarian" "XL" pizza to "some street 7, 55", with extra: "cheese, onion"
    Then order is created
