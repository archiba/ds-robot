from dsrobo.env import OS_GUI_NAME

if OS_GUI_NAME == "MacOS":
    from .mac import JobActionPipelineBase as JobActionPipelineBaseMacOS

    JobActionPipelineBase = JobActionPipelineBaseMacOS
elif OS_GUI_NAME == "LinuxGTK":
    from .linux_gtk import JobActionPipelineBase as JobActionPipelineBaseLinuxGTK

    JobActionPipelineBase = JobActionPipelineBaseLinuxGTK
else:
    raise ValueError("OS_GUI_NAME must be either 'MacOS' or 'LinuxGTK'")
