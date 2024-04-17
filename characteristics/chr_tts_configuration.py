import json
import os
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrTTSConfiguration(Characteristic):
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
                    "tts_model": aily.get_tts_model(),
                    "tts_key": aily.get_tts_key(),
                    "tts_role": aily.get_tts_role(),
                }
                self._value = bytes(json.dumps(data), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSConfiguration - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrTTSConfiguration - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            for key, value in data.items():
                if key == "tts_model":
                    aily.set_tts_model(value)
                elif key == "tts_key":
                    aily.set_tts_key(value)
                elif key == "tts_role":
                    aily.set_tts_role(value)

            aily.save()

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrTTSConfiguration - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
