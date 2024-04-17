import os

from dotenv import set_key, load_dotenv
from loguru import logger


class AilyCtl:
    aily_conf_path = None
    aily_supervisor_name = None

    def load_aily_conf(self):
        aily_conf_path = os.environ.get("AILY_ENV_PATH")
        if aily_conf_path is None:
            logger.warning("AILY_ENV_PATH is not set")
            return False

        aily_supervisor_name = os.environ.get("AILY_SUPERVISOR_NAME")
        if aily_supervisor_name is None:
            logger.warning("AILY_SUPERVISOR_NAME is not set")
            return False
        else:
            self.aily_supervisor_name = aily_supervisor_name

        if load_dotenv(aily_conf_path):
            self.aily_conf_path = aily_conf_path
            return True
        else:
            logger.error("Failed to load AILY_ENV_PATH")
            return False

    def __init__(self) -> None:
        load_res = self.load_aily_conf()
        if not load_res:
            raise RuntimeError("Failed to load AILY_CONF_PATH")

    def get_llm_model(self):
        return os.getenv("LLM_MODEL", "")

    def set_llm_model(self, value):
        os.environ["LLM_MODEL"] = value
        set_key(self.aily_conf_path, "LLM_MODEL", value)
        return True

    def get_llm_key(self):
        return os.getenv("LLM_KEY", "")

    def set_llm_key(self, value):
        os.environ["LLM_KEY"] = value
        set_key(self.aily_conf_path, "LLM_KEY", value)
        return True

    def get_llm_preprompt(self):
        return os.getenv("LLM_PRE_PROMPT", "")

    def set_llm_preprompt(self, value):
        os.environ["LLM_PRE_PROMPT"] = value
        set_key(self.aily_conf_path, "LLM_PRE_PROMPT", value)
        return True

    def get_llm_temp(self):
        return os.getenv("LLM_TEMPERATURE", "")

    def set_llm_temp(self, value):
        os.environ["LLM_TEMPERATURE"] = value
        set_key(self.aily_conf_path, "LLM_TEMPERATURE", value)
        return True

    def get_stt_model(self):
        return os.getenv("STT_MODEL", "")

    def set_stt_model(self, value):
        os.environ["STT_MODEL"] = value
        set_key(self.aily_conf_path, "STT_MODEL", value)
        return True

    def get_stt_key(self):
        return os.getenv("STT_KEY", "")

    def set_stt_key(self, value):
        os.environ["STT_KEY"] = value
        set_key(self.aily_conf_path, "STT_KEY", value)
        return True

    def get_tts_model(self):
        return os.getenv("TTS_MODEL", "")

    def set_tts_model(self, value):
        os.environ["TTS_MODEL"] = value
        set_key(self.aily_conf_path, "TTS_MODEL", value)
        return True

    def get_tts_key(self):
        return os.getenv("TTS_KEY", "")

    def set_tts_key(self, value):
        os.environ["TTS_KEY"] = value
        set_key(self.aily_conf_path, "TTS_KEY", value)
        return True

    def get_tts_role(self):
        return os.getenv("TTS_ROLE", "")

    def set_tts_role(self, value):
        os.environ["TTS_ROLE"] = value
        set_key(self.aily_conf_path, "TTS_ROLE", value)
        return True

    def save(self):
        # 重启aily服务
        os.system(f"sudo supervisorctl stop {self.aily_supervisor_name}")
        os.system(f"sudo supervisorctl start {self.aily_supervisor_name}")
