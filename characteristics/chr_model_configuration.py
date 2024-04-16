import json
import os
from pybleno import Characteristic
from loguru import logger
from aily import CtlAily


class ChrModelConfiguration(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read", "write", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            aily = CtlAily()
            data = {
                "model": aily.get_llm_model(),
                "key": aily.get_llm_key(),
                "pre_prompt": aily.get_llm_preprompt(),
                "temperature": aily.get_llm_temp(),
            }
            self._value = bytes(json.dumps(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrModelConfiguration - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrModelConfiguration - onWriteRequest: value = " + str(data))

            aily = CtlAily()
            for key, value in data.items():
                if key == "model":
                    aily.set_llm_model(value)
                elif key == "key":
                    aily.set_llm_key(value)
                elif key == "pre_prompt":
                    aily.set_llm_preprompt(value)
                elif key == "temperature":
                    aily.set_llm_temp(value)

            aily.save()
            
            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrModelConfiguration - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
