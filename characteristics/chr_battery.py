import psutil
from pybleno import Characteristic


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
        data = self.get_battery()
        print("ChrBattery - onReadRequest: value = " + str(data))
        self._value = bytes(str(data), "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_battery():
        battery = psutil.sensors_battery()
        return battery.percent
