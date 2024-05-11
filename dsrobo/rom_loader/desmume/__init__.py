from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import DeSmuMERomLoader as DeSmuMERomLoaderMac
    DeSmuMERomLoader = DeSmuMERomLoaderMac
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import DeSmuMERomLoader as DeSmuMERomLoaderLinuxGTK
    DeSmuMERomLoader = DeSmuMERomLoaderLinuxGTK
else:
    raise ValueError("OS_GUI_NAME must be either MacOS or LinuxGTK")
