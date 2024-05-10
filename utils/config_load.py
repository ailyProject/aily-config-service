import yaml
import os


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ConfigLoad:
    def __init__(self):
        self.config = os.getenv("AILY_CONFIG_PATH")
        self.data = None
        self.load_config()

    def load_config(self):
        if self.data is None:
            with open(self.config, "r") as f:
                self.data = yaml.safe_load(f)

    def get_llm_models(self):
        return self.data["llm"]["models"]

    def get_stt_models(self):
        return self.data["stt"]["models"]

    def get_tts_models(self):
        return self.data["tts"]["models"]
