from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import (
        CommonTerminate as CommonTerminateMacOS,
        CommonFindWindow as CommonFindWindowMacOS,
        CommonFindElementByRole as CommonFindElementByRoleMacOS,
        CommonTakeScreenshot as CommonTakeScreenshotMacOS,
        CommonSendHotkey as CommonSendHotkeyMacOS,
        CommonSendControl as CommonSendControlMacOS,
        CommonTypeWrite as CommonTypeWriteMacOS,
    )

    CommonTerminate = CommonTerminateMacOS
    CommonFindWindow = CommonFindWindowMacOS
    CommonFindElementByRole = CommonFindElementByRoleMacOS
    CommonTakeScreenshot = CommonTakeScreenshotMacOS
    CommonSendHotkey = CommonSendHotkeyMacOS
    CommonSendControl = CommonSendControlMacOS
    CommonTypeWrite = CommonTypeWriteMacOS
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import (
        CommonTerminate as CommonTerminateLinuxGtk,
        CommonFindWindow as CommonFindWindowLinuxGtk,
        CommonFindElementByRole as CommonFindElementByRoleLinuxGtk,
        CommonTakeScreenshot as CommonTakeScreenshotLinuxGtk,
        CommonSendHotkey as CommonSendHotkeyLinuxGtk,
        CommonSendControl as CommonSendControlLinuxGtk,
        CommonTypeWrite as CommonTypeWriteLinuxGtk,
    )

    CommonTerminate = CommonTerminateLinuxGtk
    CommonTakeScreenshot = CommonTakeScreenshotLinuxGtk
    CommonFindWindow = CommonFindWindowLinuxGtk
    CommonFindElementByRole = CommonFindElementByRoleLinuxGtk
    CommonSendHotkey = CommonSendHotkeyLinuxGtk
    CommonSendControl = CommonSendControlLinuxGtk
    CommonTypeWrite = CommonTypeWriteLinuxGtk
else:
    raise ValueError("Unknown OS_GUI_NAME was specified.")

common_action_set = \
    [
        CommonTerminate,
        CommonFindWindow,
        CommonFindElementByRole
    ] + \
    [
        CommonTakeScreenshot,
    ] + \
    [
        CommonSendHotkey,
        CommonSendControl,
        CommonTypeWrite
    ]
