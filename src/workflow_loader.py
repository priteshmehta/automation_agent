import os
import yaml
import json
from jinja2 import Template

class WorkflowLoader:
    def __init__(self, main_path, variables=None):
        self.main_path = main_path
        self.common_dir = os.path.join(os.path.dirname(main_path), "common")
        self.variables = variables or {}
    
    def _render_template(self, data):
        if isinstance(data, str):
            return Template(data).render(**self.variables)
        elif isinstance(data, list):
            return [self._render_template(item) for item in data]
        elif isinstance(data, dict):
            return {k: self._render_template(v) for k, v in data.items()}
        return data
    
    def load_combined_workflow(self):
        with open(self.main_path, "r") as f:
            main_data = yaml.safe_load(f)

        if not os.path.exists(self.common_dir):
            return main_data

        for section in ["setup", "cleanup"]:
            alias = main_data.get(section)
            if isinstance(alias, str):
                shared_path = os.path.join(self.common_dir, f"{alias}.yaml")
                if os.path.exists(shared_path):
                    with open(shared_path, "r") as f:
                        shared_steps = yaml.safe_load(f)
                        main_data[section] = shared_steps.get(alias, shared_steps)

        return self._render_template(main_data)
    
    def get_goals(self, step: list) -> list:
        """ Function to load a test case from a YAML file. 
        Args:
            step (str): The name of the test case to load.
        Returns:        
        """
        goals = [item['goal'] for item in step if 'goal' in item.keys()] 
        return goals