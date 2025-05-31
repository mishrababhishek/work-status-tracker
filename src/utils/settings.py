from .logger import log
from typing import Literal
import os
import json

__CONFIG_KEYS = Literal["repos", "models", "default_model"]

current_dir = os.path.dirname(os.path.abspath(__file__))
settings_path = os.path.join(current_dir, "..", "..", "settings.json")


def get_config(key: __CONFIG_KEYS | None = None):
    log(f"[get_config] Called with key: {key}")

    if key is None:
        log("[get_config] No key provided. Returning None.")
        return None

    if key not in __CONFIG_KEYS.__args__:
        log(f"[get_config] Invalid key '{key}' provided. Valid keys: {__CONFIG_KEYS.__args__}")
        return None

    log(f"[get_config] Attempting to read config file from: {settings_path}")

    try:
        with open(settings_path, "r") as config_file:
            log("[get_config] Opened settings.json successfully.")
            config = json.load(config_file)
            log("[get_config] Parsed JSON config successfully.")

            value = config.get(key)
            if value is not None:
                log(f"[get_config] Found value for key '{key}': {value}")
            else:
                log(f"[get_config] Key '{key}' not found in configuration.")

            return value

    except FileNotFoundError:
        log(f"[get_config] Configuration file not found at: {settings_path}")
    except json.JSONDecodeError as jde:
        log(f"[get_config] JSON decode error: {jde}")
    except Exception as e:
        log(f"[get_config] Unexpected error loading configuration: {e}")

    return None
