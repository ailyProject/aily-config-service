import psutil
from pybleno import Characteristic
from loguru import logger


class ChrRamUsage(Characteristic):
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
            data = self.get_ram_usage()
            logger.info("ChrRAMUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrRAMUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_ram_usage():
        ram_usage = psutil.virtual_memory().percent
        return ram_usage
