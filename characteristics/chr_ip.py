import socket
import array

from pybleno import Characteristic


class ChrIP(Characteristic):
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

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "127.0.0.1"
        finally:
            s.close()
        return IP

    def onReadRequest(self, offset, callback):
        ip_address = self.get_ip()
        print("ChrIP - onReadRequest: value = " + str(ip_address))
        # 获取当前ip地址
        self._value = bytes(ip_address, "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)
