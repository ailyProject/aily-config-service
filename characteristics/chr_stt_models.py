import os
import yaml
import json
from pybleno import Characteristic
from loguru import logger


class ChrSTTModels(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_conf()
            logger.info("ChrSTTModels - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrSTTModels - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        conf_file = os.getenv("AILY_CONFIG_PATH")
        with open(conf_file, "r") as f:
            conf = yaml.safe_load(f)
        return json.dumps(conf["stt"]["models"])
