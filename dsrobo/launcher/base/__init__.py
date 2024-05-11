from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import EmulatorLauncherBase as EmulatorLauncherBaseMac
    EmulatorLauncherBase = EmulatorLauncherBaseMac
elif OS_GUI_NAME == "LinuxGTK":
    pass
