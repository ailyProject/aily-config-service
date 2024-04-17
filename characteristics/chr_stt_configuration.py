import json
import os
from pybleno import Characteristic
from loguru import logger
from aily import CtlAily


class ChrSTTConfiguration(Characteristic):
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
                aily = CtlAily()
                data = {
                    "stt_model": aily.get_stt_model(),
                    "stt_key": aily.get_stt_key(),
                }
                self._value = bytes(json.dumps(data), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrSTTConfiguration - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrSTTConfiguration - onWriteRequest: value = " + str(data))

            aily = CtlAily()
            for key, value in data.items():
                if key == "stt_model":
                    aily.set_stt_model(value)
                elif key == "stt_key":
                    aily.set_stt_key(value)

            aily.save()

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrSTTConfiguration - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
