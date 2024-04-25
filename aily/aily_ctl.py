import os
import sqlite3

from dotenv import set_key, load_dotenv
from loguru import logger
from pathlib import Path


class AilyCtl:
    aily_path = None
    aily_env_path = None
    aily_supervisor_name = None

    def load_aily_conf(self):
        aily_path = os.environ.get("AILY_PATH")
        if aily_path is None:
            logger.warning("AILY_PATH is not set")
            return False
        else:
            self.aily_path = aily_path

        aily_env_path = os.environ.get("AILY_ENV_PATH")
        if aily_env_path is None:
            logger.warning("AILY_ENV_PATH is not set")
            return False

        aily_supervisor_name = os.environ.get("AILY_SUPERVISOR_NAME")
        if aily_supervisor_name is None:
            logger.warning("AILY_SUPERVISOR_NAME is not set")
            return False
        else:
            self.aily_supervisor_name = aily_supervisor_name

        if load_dotenv(aily_env_path):
            self.aily_env_path = aily_env_path
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
        res, k, v = set_key(self.aily_env_path, "LLM_MODEL", value)
        return res

    def get_llm_key(self):
        return os.getenv("LLM_KEY", "")

    def set_llm_key(self, value):
        os.environ["LLM_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_KEY", value)
        return res

    def get_llm_preprompt(self):
        return os.getenv("LLM_PRE_PROMPT", "")

    def set_llm_preprompt(self, value):
        os.environ["LLM_PRE_PROMPT"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_PRE_PROMPT", value)
        return res

    def get_llm_temp(self):
        return os.getenv("LLM_TEMPERATURE", "")

    def set_llm_temp(self, value):
        os.environ["LLM_TEMPERATURE"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_TEMPERATURE", value)
        return res

    def get_stt_model(self):
        return os.getenv("STT_MODEL", "")

    def set_stt_model(self, value):
        os.environ["STT_MODEL"] = value
        res, k, v = set_key(self.aily_env_path, "STT_MODEL", value)
        return res

    def get_stt_key(self):
        return os.getenv("STT_KEY", "")

    def set_stt_key(self, value):
        os.environ["STT_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "STT_KEY", value)
        return res

    def get_tts_model(self):
        return os.getenv("TTS_MODEL", "")

    def set_tts_model(self, value):
        os.environ["TTS_MODEL"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_MODEL", value)
        return res

    def get_tts_key(self):
        return os.getenv("TTS_KEY", "")

    def set_tts_key(self, value):
        os.environ["TTS_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_KEY", value)
        return res

    def get_tts_role(self):
        return os.getenv("TTS_ROLE", "")

    def set_tts_role(self, value):
        os.environ["TTS_ROLE"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_ROLE", value)
        return res

    def save(self):
        # 重启aily服务
        os.system(f"sudo supervisorctl stop {self.aily_supervisor_name}")
        os.system(f"sudo supervisorctl start {self.aily_supervisor_name}")

    def get_logs(self, page=1, page_size=1):
        if not os.environ.get("DB_NAME"):
            return []

        if not os.path.isabs(os.environ.get("DB_NAME")):
            # aily_path = Path(self.aily_path).parent
            db_path = os.path.abspath(
                os.path.join(self.aily_path, os.environ.get("DB_NAME"))
            )
        else:
            db_path = os.environ.get("DB_NAME")

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM conversations")
        total = cursor.fetchone()[0]
        if total == 0 or total < (page - 1) * page_size:
            return []

        cursor.execute(
            "SELECT role, msg FROM conversations ORDER BY created_at ASC LIMIT ? OFFSET ?",
            (page_size, (page - 1) * page_size),
        )
        return cursor.fetchall()
