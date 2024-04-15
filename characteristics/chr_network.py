import psutil
from pybleno import Characteristic
from loguru import logger
import re


class ChrNetwork(Characteristic):
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
            data = self.get_network()
            logger.info("ChrNetwork - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrNetwork - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_network():
        # TODO: Implement this method
        net_status_list = psutil.net_if_stats()
        # 当前网络接口
        current_net = None
        for key, value in net_status_list.items():
            if re.match(r"^lo", key):
                continue
            if value.isup:
                current_net = key

        if current_net is None:
            return "无"
        elif re.match(r"^wlan", current_net):
            return "WiFi"
        elif re.match(r"^eth", current_net):
            return "有线"
        else:
            return "UNKNOWN"
