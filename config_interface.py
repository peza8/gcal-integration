from typing import List
import json


class ConfigInterface:
    CONFIG_FILE_PATH = "config.json"

    def __init__(self) -> None:
        self.config = self._load_config_json()

    def get_calendar_ids(self) -> List[str]:
        return self.config["calendar_ids"]

    def _load_config_json(self) -> str:
        with open(self.CONFIG_FILE_PATH, 'r') as config_file:
            config_data = json.load(config_file)
            return config_data

config_interface = ConfigInterface()