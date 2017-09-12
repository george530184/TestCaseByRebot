*** Settings ***
Library           Selenium2Library
Resource          testflow.txt

*** Variables ***
${guide_upgrade_times}    3

*** Test Cases ***
Upgrade_by_GuideWeb
    Comment    Upgrade by Guide Web    should change eth0->br-guide
    :FOR    ${i}    IN RANGE    ${guide_upgrade_times}
    \    log    'Guide_Upgrade Test! ${i}+1'
    \    guide_upgrade_by_file
