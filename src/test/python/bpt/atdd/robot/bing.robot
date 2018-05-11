*** Settings ***
Library    bpt.atdd.keywords.SearchKeywords

*** Variables ***
${browser}      firefox
${is_remote}        ${False}
${url}      http://cn.bing.com
${keyword}    wesleypeng+uiXautomation

*** Test Cases ***
[TC1] - Validate basic features of web UI test automation framework
    [Documentation]    As an automation engineer, I want to validate the web controls are working properly
    ...     So that I can perform web ui automated testing
    [Tags]  bing.ui
    [Setup]  Launch Browser    ${browser}    ${is_remote}
    [Teardown]  Close Browser
    Given I Am On Home Page     ${url}
    When I Search With Keyword      ${keyword}
    Then I Get The Keyword Is Displayed On Search Results       ${keyword}
