import psutil
from pybleno import Characteristic


class ChrRamUsage(Characteristic):
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
        data = self.get_ram_usage()
        print("ChrRAMUsage - onReadRequest: value = " + str(data))
        self._value = bytes(str(data), "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_ram_usage():
        ram_usage = psutil.virtual_memory().percent
        return ram_usage
