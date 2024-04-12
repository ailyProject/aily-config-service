import psutil
from pybleno import Characteristic


class ChrCpuUsage(Characteristic):
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
        usage = self.get_cpu_usage()
        print("ChrCpuUsage - onReadRequest: value = " + str(usage))
        self._value = bytes(str(usage), "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_cpu_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        return cpu_usage
