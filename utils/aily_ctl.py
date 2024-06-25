import os
import sqlite3
import re

from dotenv import set_key, load_dotenv
from loguru import logger
from pathlib import Path
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
class AilyCtl:
    _instance = None
    aily_path = None
    aily_env_path = None
    aily_supervisor_name = None

    # @staticmethod
    # def get_instance():
    #     if AilyCtl._instance is None:
    #         AilyCtl._instance = AilyCtl()
    #     return AilyCtl._instance

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
        self.log_cur_page = 0
        self.start_get_logs = False
        load_res = self.load_aily_conf()
        if not load_res:
            pass
            # raise RuntimeError("Failed to load AILY_CONF_PATH")
        # if AilyCtl._instance is not None:
        #     pass
        # else:
        #     load_res = self.load_aily_conf()
        #     if not load_res:
        #         pass
        #         # raise RuntimeError("Failed to load AILY_CONF_PATH")
        #     AilyCtl._instance = self

    def get_llm_url(self):
        return os.getenv("LLM_URL", "")

    def set_llm_url(self, value):
        if not value:
            value = ""

        os.environ["LLM_URL"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_URL", value)
        return res

    def get_llm_model(self):
        return os.getenv("LLM_MODEL") or ""

    def set_llm_model(self, value):
        if not value:
            value = ""
            
        os.environ["LLM_MODEL"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_MODEL", value)
        return res

    def get_llm_key(self):
        return os.getenv("LLM_KEY") or ""

    def set_llm_key(self, value):
        if not value:
            value = ""

        os.environ["LLM_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_KEY", value)
        return res

    def get_llm_preprompt(self):
        return os.getenv("LLM_PRE_PROMPT") or ""

    def set_llm_preprompt(self, value):
        if not value:
            value = ""

        os.environ["LLM_PRE_PROMPT"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_PRE_PROMPT", value)
        return res

    def get_llm_temp(self):
        return os.getenv("LLM_TEMPERATURE") or ""

    def set_llm_temp(self, value):
        if not value:
            value = ""
        
        os.environ["LLM_TEMPERATURE"] = value
        res, k, v = set_key(self.aily_env_path, "LLM_TEMPERATURE", value)
        return res

    def get_stt_url(self):
        return os.getenv("STT_URL") or ""

    def set_stt_url(self, value):
        if not value:
            value = ""

        os.environ["STT_URL"] = value
        res, k, v = set_key(self.aily_env_path, "STT_URL", value)
        return res

    def get_stt_model(self):
        return os.getenv("STT_MODEL") or ""

    def set_stt_model(self, value):
        if not value:
            value = ""
    
        os.environ["STT_MODEL"] = value
        res, k, v = set_key(self.aily_env_path, "STT_MODEL", value)
        return res

    def get_stt_key(self):
        return os.getenv("STT_KEY") or ""

    def set_stt_key(self, value):
        if not value:
            value = ""

        os.environ["STT_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "STT_KEY", value)
        return res

    def get_tts_url(self):
        return os.getenv("TTS_URL") or ""

    def set_tts_url(self, value):
        if not value:
            value = ""

        os.environ["TTS_URL"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_URL", value)
        return res

    def get_tts_model(self):
        return os.getenv("TTS_MODEL") or ""

    def set_tts_model(self, value):
        if not value:
            value = ""
            
        os.environ["TTS_MODEL"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_MODEL", value)
        return res

    def get_tts_key(self):
        return os.getenv("TTS_KEY") or ""

    def set_tts_key(self, value):
        if not value:
            value = ""
            
        os.environ["TTS_KEY"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_KEY", value)
        return res

    def get_tts_role(self):
        return os.getenv("TTS_ROLE") or ""

    def set_tts_role(self, value):
        if not value:
            value = ""

        os.environ["TTS_ROLE"] = value
        res, k, v = set_key(self.aily_env_path, "TTS_ROLE", value)
        return res

    def save(self, value):
        # 重启aily服务
        try:
            os.system(f"sudo supervisorctl stop {self.aily_supervisor_name}")
            os.system(f"sudo supervisorctl start {self.aily_supervisor_name}")
            return True
        except Exception as e:
            logger.error(f"aily save err: {e}")
            return False
    
    def get_log(self):
        logger.debug("get_first_log")
        if self.start_get_logs is False:
            self.start_get_logs = True
            self.log_cur_page += 1

    def get_logs(self, page_size=10):
        if not os.environ.get("DB_NAME"):
            return None

        if not os.path.isabs(os.environ.get("DB_NAME")):
            # aily_path = Path(self.aily_path).parent
            db_path = os.path.abspath(
                os.path.join(self.aily_path, os.environ.get("DB_NAME"))
            )
        else:
            db_path = os.environ.get("DB_NAME")

        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()

            cursor.execute("SELECT COUNT(*) FROM conversations")
            total = cursor.fetchone()[0]
            if total == 0 or total < (self.log_cur_page - 1) * page_size:
                return None

            cursor.execute(
                "SELECT role, msg, msg_type FROM conversations ORDER BY created_at DESC LIMIT ? OFFSET ?",
                (page_size, (self.log_cur_page - 1) * page_size),
            )

            fetchdata = cursor.fetchall()
            self.start_get_logs = False
            
            return fetchdata
            # if fetchdata:
            #     # data = {"role": fetchdata[0][0], "msg": fetchdata[0][1]}
            #     data = str(fetchdata[0][0]) + ":" + str(fetchdata[0][1])
            #     return data

            # return None
        except Exception as e:
            logger.error(f"get_logs: {e}")
            return None

    def get_status(self):
        # 获取superivsor中aily服务的状态
        try:
            output = os.popen(
                f"sudo supervisorctl status {self.aily_supervisor_name}"
            ).read()
            match = re.search(r"\b(RUNNING|STOPPED|STARTING|EXITED)\b", output)
            if match:
                status = match.group(0)
            else:
                status = "N/A"
            return status
        except Exception as e:
            logger.error(f"get_status: {e}")
            return "N/A"
