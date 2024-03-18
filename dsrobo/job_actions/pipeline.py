import uuid
from pathlib import Path

from atomacos import NativeUIElement

from dsrobo.config import JobConfig, EmulatorTypes, JobActionConfig, Config
from dsrobo.job_actions.citra import dependent_action_set as citra_action_set
from dsrobo.job_actions.common import common_action_set
from dsrobo.job_actions.desmume import dependent_action_set as desmume_action_set
from dsrobo.job_actions.states import JobActionStates, JobFileOutput
from dsrobo.utils import find_window_by_exact_name


class JobActionPipelineBase(object):

    def __init__(self, config: Config, job_config: JobConfig):
        self.config = config
        self.job_config = job_config
        if self.job_config.emulator_type == EmulatorTypes.NintendoDS:
            self.registered_actions = common_action_set + desmume_action_set
            self.emulator_config = config.desmume
        else:
            self.registered_actions = common_action_set + citra_action_set
            self.emulator_config = config.citra
        self.registered_action_map = {action.name: action for action in self.registered_actions}
        self.execution_id = f"{self.job_config.job_name}-{uuid.uuid4()}"
        self.states = JobActionStates()
        self.dest_root_dir = Path(config.dest_directory).absolute() / self.execution_id

    def _validate(self, actions: list[JobActionConfig]):
        for action in actions:
            if action.action_type not in self.registered_action_map.keys():
                raise ValueError(f"Invalid action name: {action.action_type}")
            action_obj = self.registered_action_map[action.action_type]()
            action_obj.validate(action.action_parameters, action.then.keys())
            for status_code, nested_actions in action.then.items():
                self._validate(nested_actions)

    def validate(self):
        self._validate(self.job_config.actions)

    def register_reserved_elements(self, application: NativeUIElement):
        self.states.elements['application'] = application
        self.states.elements['menu_bar'] = getattr(application, 'AXMenuBar')
        self.states.elements['main_window'] = find_window_by_exact_name(application,
                                                                        self.emulator_config.main_window_name)

    def _run_single_action(self, action: JobActionConfig, dest: Path):
        action_obj = self.registered_action_map[action.action_type]()
        app = self.states.elements['application']
        element = self.states.elements[action.target_element]
        status, result = action_obj(self.states, JobFileOutput(dest), app, element, action.action_parameters)
        print(action.then.keys())
        next_actions = action.then.get(int(status), None)
        if next_actions is None:
            return
        self._run_series_of_actions(next_actions, dest)

    def _run_action(self, action: JobActionConfig, dest_root: Path):
        if action.n_repeats is None:
            return self._run_single_action(action, dest_root)
        else:
            for i in range(action.n_repeats):
                dest_root_ = dest_root / f"{i}"
                self._run_single_action(action, dest_root_)
        return

    def _run_series_of_actions(self, actions: list[JobActionConfig], dest_root: Path):
        for i, action in enumerate(actions):
            action_name = f"{i}_{action.action_name}_{str(action.action_type)}"
            self._run_action(action, dest_root / action_name)
        return

    def __call__(self, application: NativeUIElement):
        self.register_reserved_elements(application)
        self._run_series_of_actions(self.job_config.actions, self.dest_root_dir)
