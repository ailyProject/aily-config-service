import psutil
from pybleno import Characteristic


class ChrPower(Characteristic):
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
        data = self.get_power()
        print("ChrPower - onReadRequest: value = " + str(data))
        self._value = bytes(str(data), "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_power():
        # TODO: Implement this method
        battery = psutil.sensors_battery()
        return battery.percent
