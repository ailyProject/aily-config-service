import psutil
from pybleno import Characteristic
from loguru import logger


class ChrDiskUsage(Characteristic):
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
            data = self.get_disk_usage()
            logger.info("ChrDiskUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrDiskUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_disk_usage():
        disk_usage = psutil.disk_usage("/").percent
        return disk_usage
