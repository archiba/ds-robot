from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import DeSmuMEReset as DeSmuMEResetMacOS
    from .mac import DeSmuMESaveStateFile as DeSmuMESaveStateFileMacOS

    DeSmuMEReset = DeSmuMEResetMacOS
    DeSmuMESaveStateFile = DeSmuMESaveStateFileMacOS
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import DeSmuMEReset as DeSmuMEResetLinuxGTK
    from .linux_gtk import DeSmuMESaveStateFile as DeSmuMESaveStateFileLinuxGTK

    DeSmuMEReset = DeSmuMEResetLinuxGTK
    DeSmuMESaveStateFile = DeSmuMESaveStateFileLinuxGTK
else:
    raise ValueError("Unknown OS_GUI_NAME was specified.")

dependent_action_set = [
    DeSmuMEReset, DeSmuMESaveStateFile
]
