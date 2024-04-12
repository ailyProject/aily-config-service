import psutil
from pybleno import Characteristic


class ChrDiskUsage(Characteristic):
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
        data = self.get_disk_usage()
        print("ChrDiskUsage - onReadRequest: value = " + str(data))
        self._value = bytes(str(data), "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_disk_usage():
        disk_usage = psutil.disk_usage("/").percent
        return disk_usage
