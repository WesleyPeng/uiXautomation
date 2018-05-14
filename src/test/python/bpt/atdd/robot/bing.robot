*** Settings ***
Library    bpt.atdd.keywords.SearchKeywords

*** Variables ***
${browser}      firefox
${is_remote}        ${False}
${enable_screenshot}    ${False}
${url}      http://cn.bing.com
${keyword}    wesleypeng+uiXautomation

*** Test Cases ***
[TC1] - Validate basic features of web UI test automation framework
    [Documentation]    As an automation engineer, I want to validate the web controls are working properly
    ...     So that I can perform web ui automated testing
    [Tags]  bing.ui
    [Setup]  Launch Browser    ${browser}    ${is_remote}   ${enable_screenshot}
    [Teardown]  Close Browser
    Given I Am On Home Page     ${url}
    When I Search With Keyword      ${keyword}
    Then I Get The First Search Record Containing Keyword       ${keyword}
