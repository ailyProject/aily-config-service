from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrAilyReload(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["write", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrAily - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.save()

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrSttModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
