@api
Feature: Validate REST Client plugin implemented with Python requests
  In order to perform API level automated testing,
  As a software testing engineer
  I want to validate that the REST Client is runnable

  Scenario Outline: Perform operation against the API server
    Given I have the API server url "<url>"
    When I perform action "<action>" on the resource "<resource>" without payload
    Then I get the status code "<status_code>"
    And  I also get the key value pair "<key>" "<value>" in response

    Examples: httpbin
    | url                 | action | resource | status_code | key      | value |
    | http://httpbin.org  | GET    | deflate  | 200         | deflated | True  |
    | http://httpbin.org  | GET    | anything | 200         | method   | GET   |
