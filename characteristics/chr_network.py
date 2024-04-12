from pybleno import Characteristic
from loguru import logger


class ChrNetwork(Characteristic):
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
            data = self.get_network()
            logger.info("ChrNetwork - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrNetwork - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_network():
        # TODO: Implement this method
        return None
