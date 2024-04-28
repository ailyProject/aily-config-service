import json
import os
import yaml
import time
import threading
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrTTSModel(Characteristic):
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
                self._value = bytes(aily.get_tts_model(), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSModel - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = data.decode("utf-8")
            logger.info("ChrTTSModel - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_tts_model(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrTTSModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrTTSRole(Characteristic):
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
                self._value = bytes(aily.get_tts_role(), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSRole - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = data.decode("utf-8")
            logger.info("ChrTTSRole - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_tts_role(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrTTSRole - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrTTSKey(Characteristic):
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
                self._value = bytes(aily.get_tts_key(), "utf8")
                callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSKey - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            data = data.decode("utf-8")
            logger.info("ChrTTSKey - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_tts_key(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrTTSKey - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)


class ChrTTSModelOptions(Characteristic):
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
            logger.info("ChrTTSModelOptions - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSModelOptions - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        try:
            conf_file = os.getenv("AILY_CONFIG_PATH")
            with open(conf_file, "r") as f:
                conf = yaml.safe_load(f)
            return conf["tts"]["models"]
        except Exception as e:
            return "N/A"
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrTTSModelOptions - onSubscribe")
        self._updateValueCallback = updateValueCallback
        self.start_sending()

    def onUnsubscribe(self):
        logger.info("ChrTTSModelOptions - onUnsubscribe")
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
        if records:
            logger.info("ChrTTSModelOptions - loop_get: value = " + str(records))
            self._value = bytes(json.dumps(records), "utf-8")
            # 判断self._value的长度，如果超过120字节，就分段发送
            for model in records:
                send_data = model["name"] + ":" + model["value"]
                logger.info("model: {0}".format(send_data))
                self._updateValueCallback(send_data.encode("utf-8"))
                time.sleep(0.1)

            # self._updateValueCallback(self._value)
            self._updateValueCallback(bytes("\n", "utf-8"))

        self.stop_sending()


class ChrTTSRoleOptions(Characteristic):
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
            logger.info("ChrTTSRoleOptions - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrTTSRoleOptions - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        try:
            conf_file = os.getenv("AILY_CONFIG_PATH")
            with open(conf_file, "r") as f:
                conf = yaml.safe_load(f)
            return conf["tts"]["roles"]
            # return json.dumps(conf["tts"]["roles"])
        except Exception as e:
            return "N/A"
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrTTSRoleOptions - onSubscribe")
        self._updateValueCallback = updateValueCallback
        self.start_sending()

    def onUnsubscribe(self):
        logger.info("ChrTTSRoleOptions - onUnsubscribe")
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
            logger.info("ChrTTSRoleOptions - loop_get: value = " + str(records))
            self._value = bytes(json.dumps(records), "utf-8")
            # 判断self._value的长度，如果超过120字节，就分段发送
            for model in records:
                logger.info("model: {0}".format(model))
                send_data = model["name"] + ":" + model["value"]
                logger.info("model: {0}".format(send_data))
                self._updateValueCallback(send_data.encode("utf-8"))

            # self._updateValueCallback(self._value)
        else:
            self._updateValueCallback("[]".encode("utf-8"))
        
        self._updateValueCallback(bytes("\n", "utf-8"))
        self.stop_sending()