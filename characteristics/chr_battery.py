import psutil
from pybleno import Characteristic
from loguru import logger


class ChrBattery(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_battery()
            logger.info("ChrBattery - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrBattery - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_battery():
        battery = psutil.sensors_battery()
        return battery.percent
