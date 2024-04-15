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
                "properties": ["read", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            hostname = self.get_mac()
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
        # 获取 MAC 地址
        mac = uuid.getnode()
        # 转换为常见的 MAC 地址格式
        mac_address = ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
        return mac_address
