import json
import os
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrLLMConfiguration(Characteristic):
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
            if self._value:
                callback(Characteristic.RESULT_SUCCESS, self._value)
            else:
                aily = AilyCtl()
                data = {
                    "llm_model": aily.get_llm_model(),
                    "llm_key": aily.get_llm_key(),
                    "llm_preprompt": aily.get_llm_preprompt(),
                    "llm_temp": aily.get_llm_temp(),
                }
                self._value = bytes(json.dumps(data), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMModelConfiguration - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrLLMModelConfiguration - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            for key, value in data.items():
                if key == "llm_model":
                    aily.set_llm_model(value)
                elif key == "llm_key":
                    aily.set_llm_key(value)
                elif key == "llm_preprompt":
                    aily.set_llm_preprompt(value)
                elif key == "llm_temp":
                    aily.set_llm_temp(value)

            aily.save()

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMModelConfiguration - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
