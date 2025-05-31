from .logger import log
from typing import Literal
import os

import json

__CONFIG_KEYS = Literal["repos"]

current_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(current_dir, "..", "..", "settings.json")


def get_config(key: __CONFIG_KEYS | None = None):
    if key is None or key not in __CONFIG_KEYS.__args__:
        log("No valid key provided")

    with open(settings_path, "r") as config_file:
        try:
            log("Loading configuration from settings.json")
            config = json.load(config_file)
            return config[key]
        except Exception as e:
            log(f"Error loading configuration: {e}")
            return None
