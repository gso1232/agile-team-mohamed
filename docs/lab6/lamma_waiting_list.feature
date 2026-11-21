Feature: Automatic promotion from the waiting list
  As a student on the waiting list
  I want to be moved into a seat automatically when one frees up
  So that I don't have to keep checking

  # Team 12 Lamma - story S14 (Jira SCRUM-21), the project's key rule

  Background:
    Given an approved event "Arduino Workshop" with 2 seats

  Scenario: A seat frees up and the first person waiting gets it
    Given "Sara" and "Omar" hold the 2 seats
    And "Mona" is first and "Youssef" is second on the waiting list
    When "Sara" cancels her seat
    Then "Mona" holds a seat
    And "Youssef" is first on the waiting list
    And the event has 0 seats left

  Scenario: A student cannot take a second place in the same event
    Given "Sara" and "Omar" hold the 2 seats
    When "Sara" tries to join the waiting list
    Then the request is refused with "already has a place in this event"
    And the waiting list is empty

  Scenario Outline: Seats left after a cancellation
    Given "Sara" and "Omar" hold the 2 seats
    And <waiting> students are on the waiting list
    When "Sara" cancels her seat
    Then the event has <seats_left> seats left
    And <still_waiting> students are still waiting

    Examples:
      | waiting | seats_left | still_waiting |
      | 0       | 1          | 0             |
      | 1       | 0          | 0             |
      | 3       | 0          | 2             |
