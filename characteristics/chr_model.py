from pybleno import Characteristic
from loguru import logger


class ChrModel(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrModel - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrModel - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_llm_model():
        # TODO Implement this method
        return "GPT-3.5-Turbo"
