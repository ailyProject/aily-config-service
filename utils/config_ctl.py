import yaml
import os

from loguru import logger


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            logger.info("Creating new instance")
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@singleton
class ConfigCtl:
    def __init__(self):
        self.config = os.getenv("AILY_CONFIG_PATH")
        self.data = None
        self.load_config()
        
        self.llm_models_started = False
        self.stt_models_started = False
        self.tts_models_started = False

    def load_config(self):
        if self.data is None:
            with open(self.config, "r") as f:
                self.data = yaml.safe_load(f)

    def get_llm_models(self):
        return self.data["llm"]["models"]
    
    def get_llm_models_start(self):
        self.llm_models_started = True

    def get_stt_models(self):
        return self.data["stt"]["models"]
    
    def get_stt_models_start(self):
        self.stt_models_started = True

    def get_tts_models(self):
        return self.data["tts"]["models"]
    
    def get_tts_models_start(self):
        self.tts_models_started = True
