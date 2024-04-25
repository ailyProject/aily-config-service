import json
import threading
import time
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrAilyReload(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["write", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrAily - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.save()

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrSttModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrAilyConversation(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["notify"],
                "value": None,
            },
        )
        self._value = None
        self._timer = None
        self._page = 1
        self._perPage = 1

    def onReadRequest(self, offset, callback):
        try:
            record = self.get_logs()
            logger.info("ChrAilyConversation - onReadRequest: value = " + str(record))
            self._value = bytes(json.dumps(record), "utf-8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrAilyConversation - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrAilyConversation - onSubscribe")
        self._page = 1
        self._perPage = 1
        self._updateValueCallback = updateValueCallback
        self.start_sending()

    def onUnsubscribe(self):
        logger.info("ChrAilyConversation - onUnsubscribe")
        self._updateValueCallback = None
        self.stop_sending()

    def get_logs(self):
        aily = AilyCtl()
        return aily.get_logs(self._page, self._perPage)

    def start_sending(self, interval=0.1):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        record = self.get_logs()
        if record:
            logger.info("ChrAilyConversation - loop_get: value = " + str(record))
            result = {
                "role": record[0][0],
                "msg": record[0][1],
            }
            string_result = json.dumps(result)
            self._value = bytes(string_result, "utf-8")
            # 判断self._value的长度，如果超过120字节，就分段发送
            if len(string_result) > 60:
                for index in range(0, len(string_result), 60):
                    value = string_result[index : index + 60]
                    self._updateValueCallback(bytes(value, "utf-8"))
            else:
                self._updateValueCallback(self._value)

            self._updateValueCallback(bytes("\n", "utf-8"))

            self._page += 1
        else:
            time.sleep(10)

        self.start_sending()
