import psutil
from pybleno import Characteristic
from loguru import logger


class ChrCpuTemperature(Characteristic):
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
            temp = self.get_cpu_tempture()
            logger.info("temp: {0}".format(temp))
            logger.info("ChrCpuTemperature - onReadRequest: value = " + str(temp))
            self._value = bytes(str(temp), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrCpuTemperature - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_cpu_tempture():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
                cpu_temp = temp_file.read()
                return round(float(cpu_temp) / 1000, 2)
        except FileNotFoundError:
            return "N/A"
