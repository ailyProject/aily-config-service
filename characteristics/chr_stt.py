import json
import os
import yaml
import time
import threading
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrSTTModel(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read", "write", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            if self._value:
                callback(Characteristic.RESULT_SUCCESS, self._value)
            else:
                aily = AilyCtl()
                self._value = bytes(aily.get_stt_model(), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrSttModel - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = data.decode("utf-8")
            logger.info("ChrSttModel - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_stt_model(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrSttModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrSTTKey(Characteristic):
    def __init__(self, uuid):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read", "write", "notify"],
                "value": None,
            },
        )
        self._value = None

    def onReadRequest(self, offset, callback):
        try:
            if self._value:
                callback(Characteristic.RESULT_SUCCESS, self._value)
            else:
                aily = AilyCtl()
                self._value = bytes(aily.get_stt_key(), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrSttKey - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = data.decode("utf-8")
            logger.info("ChrSttKey - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_stt_key(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrSttKey - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrSTTModelOptions(Characteristic):
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
        self._timer = None

    def onReadRequest(self, offset, callback):
        try:
            data = json.dumps(self.get_conf())
            logger.info("ChrSTTModelOptions - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrSTTModelOptions - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        try:
            conf_file = os.getenv("AILY_CONFIG_PATH")
            with open(conf_file, "r") as f:
                conf = yaml.safe_load(f)
            return conf["stt"]["models"]
        except Exception as e:
            logger.error(f"ChrSTTModelOptions - get_conf: {e}")
            return []
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrSTTModelOptions - onSubscribe")
        self._updateValueCallback = updateValueCallback
        self.start_sending()

    def onUnsubscribe(self):
        logger.info("ChrSTTModelOptions - onUnsubscribe")
        self._updateValueCallback = None
        self.stop_sending()
    
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

        records = self.get_conf()
        if records and records != "N/A":
            logger.info("ChrSTTModelOptions - loop_get: value = " + str(records))
            self._value = bytes(json.dumps(records), "utf-8")
            # 判断self._value的长度，如果超过120字节，就分段发送
            for model in records:
                send_data = model["name"] + ":" + model["value"]
                logger.info("model: {0}".format(send_data))
                self._updateValueCallback(send_data.encode("utf-8"))
        else:
            pass
        
        self._updateValueCallback(bytes("EOF", "utf-8"))
        self.stop_sending()
