from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import DeSmuMELauncher as DeSmuMELauncherMacOS
    DeSmuMELauncher = DeSmuMELauncherMacOS
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import DeSmuMELauncher as DeSmuMELauncherLinuxGTK
    DeSmuMELauncher = DeSmuMELauncherLinuxGTK
else:
    raise ValueError("OS_GUI_NAME must be either MacOS or LinuxGTK")
