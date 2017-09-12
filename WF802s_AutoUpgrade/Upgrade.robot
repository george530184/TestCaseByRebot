*** Settings ***
Suite Setup
Test Setup
Test Teardown
Resource          testflow.txt
Library           rename.py

*** Variables ***
${device_type}    wf802gw    # incloude name: wf802gw|wf802w
${upgrade_times}    2
${item_num}       3

*** Test Cases ***
test
    [Tags]    1
    ${IP}    Ssdp Discovery
    Open Browser    http://${IP}/upgrade.html
    Select Frame    id = iframeallfirst
    Click Element    id= checkboxid
    Choose File    id = selectfile    111
    Click Button    id = BtnUpgrade
    Close All Browsers

Case 1: Rename upgrade_file
    Comment    copy file from old -> new    change name as R3.1.00.....
    Import Library    /home/share/robot_test/WF802s_AutoUpgrade/rename.py
    log    'Now We change file name by device_type'
    rename_wf802    ${device_type}

Case 2: Batch Upgrade
    [Tags]
    Comment    upgrade files from old <-->new \ many times
    : FOR    ${i}    IN RANGE    ${upgrade_times}
    \    log    'Batch Test! ${i}+1'
    \    loopfile

Case 3: Upgrade same Version
    [Tags]
    Comment    upgrade the same version
    #File mode
    reduce version
    upgrade by files    ${PATH}@{filename}[${0}]
    sleep    120s
    Select Frame    id = iframeallfirst
    Capture Page Screenshot
    ${msg}    Get Text    //*[@data-index="8"and @class="tabulator-cell "]
    Should Be Equal As Strings    ${msg}    already upgrade
    count of item
    Unselect Frame
    # OTA mode
    upgrade by ota
    upgrade_reboot_election_time
    Close Browser
    Brower_Open
    Select Frame    id = iframeallfirst
    Click Element    id= checkboxid
    Select From List    id = selectmod    ota
    ${ota_msg}    Get Element Attribute    id = BtnUpgrade@disabled
    Should Be Equal As Strings    ${ota_msg}    true
    Unselect Frame
    Close All Browsers

Case 4: Only Upgrade CAP
    [Tags]
    Comment    Only Upgrade CAP by OTA Mode
    reduce version
    Cap Is Element Exits
    upgrade_reboot_election_time
    Brower_Open
    Select Frame    id = iframeallfirst
    ${ver}    Get Text    //*[@class="tabulator-table"]/div/div/img/parent::*/parent::div/div[@data-index="3"]
    ${version}    Evaluate    ("${ver}").encode("utf-8")    # OTA Version
    ${PATH}    Set Variable    /home/share/robot_test/WF802s_AutoUpgrade/version/${device_type}/new/
    @{filename}    Evaluate    os.listdir('/home/share/robot_test/WF802s_AutoUpgrade/version/${device_type}/new/')    os
    @{current_ver}    Evaluate    os.path.splitext(${filename}[0])    os
    Should not Be Equal As Strings    ${version}    ${current_ver[0]}
    count of item
    Close Browser

Case 5: Only Upgrade RE
    [Tags]
    Comment    Only Upgrade RE By OTA Mode
    reduce version
    Re Is Element Exists
    upgrade_reboot_election_time
    Brower_Open
    Select Frame    id = iframeallfirst
    ${ver}    Get Text    //*[@data-index="1" and @data-value=""]/parent::*/div[@data-index="3"]
    ${version}    Evaluate    ("${ver}").encode("utf-8")    # OTA Version
    ${PATH}    Set Variable    /home/share/robot_test/WF802s_AutoUpgrade/version/${device_type}/new/
    @{filename}    Evaluate    os.listdir('/home/share/robot_test/WF802s_AutoUpgrade/version/${device_type}/new/')    os
    @{current_ver}    Evaluate    os.path.splitext(${filename}[0])    os
    Should not Be Equal As Strings    ${version}    ${current_ver[0]}
    count of item
    Close Browser

*** Keywords ***
