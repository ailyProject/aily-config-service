from pybleno import Characteristic


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
        data = self.get_network()
        print("ChrNetwork - onReadRequest: value = " + str(data))
        # 获取当前ip地址
        self._value = bytes(data, "utf8")
        callback(Characteristic.RESULT_SUCCESS, self._value)

    @staticmethod
    def get_network():
        # TODO: Implement this method
        return None
