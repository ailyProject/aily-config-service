import uuid
import socket
from pybleno import Characteristic
from loguru import logger


class ChrDeviceId(Characteristic):
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
            hostname = self.get_hostname()
            logger.info("ChrDeviceId - onReadRequest: value = " + hostname)
            self._value = bytes(hostname, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrDeviceId - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_mac():
        mac = ":".join(
            [
                "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
                for elements in range(0, 2 * 6, 8)
            ][::-1]
        )
        return mac
