@bing.ui
Feature: Validate basic features of web UI test automation framework
  In order to perform web UI automated testing,
  As an automation engineer
  I want to validate that the web controls are working properly

  Scenario: POM - Perform basic keyword search on cn.bing.com
    Given I am on the homepage "http://cn.bing.com"
    When I search with keyword "wesleypeng+uiXautomation"
    Then I get the first search result containing the keyword