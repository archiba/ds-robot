from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == 'MacOS':
    from .mac import JobActionBase as JobActionBaseMacOS

    JobActionBase = JobActionBaseMacOS
elif OS_GUI_NAME == 'LinuxGTK':
    from .linux_gtk import JobActionBase as JobActionBaseLinuxGTK

    JobActionBase = JobActionBaseLinuxGTK
