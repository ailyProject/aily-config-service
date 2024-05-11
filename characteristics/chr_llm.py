import os
import json
import yaml
import time
import threading
from pybleno import Characteristic
from loguru import logger
from utils import AilyCtl, ConfigLoad


class ChrLLMUrl(Characteristic):
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
            data = self.get_llm_url()
            logger.info("ChrLLMUrl - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMUrl - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrLLMUrl - onWriteRequest: value = " + str(data))
            data = data.decode("utf-8")

            if data:
                aily = AilyCtl()
                aily.set_llm_url(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMUrl - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_url():
        try:
            ctl = AilyCtl()
            return ctl.get_llm_url()
        except Exception as e:
            return "N/A"


class ChrLLMModel(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrLLMModel - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMModel - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrLLMModel - onWriteRequest: value = " + str(data))
            data = data.decode("utf-8")

            if data:
                aily = AilyCtl()
                aily.set_llm_model(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        print("EchoCharacteristic - onSubscribe")
        self._updateValueCallback = updateValueCallback

        data = self.get_llm_model()
        logger.info("ChrLLMModel - onReadRequest: value = " + str(data))
        self._value = bytes(data, "utf8")

        if self._updateValueCallback:
            self._updateValueCallback(self._value)

    def onUnsubscribe(self):
        print("EchoCharacteristic - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None

    @staticmethod
    def get_llm_model():
        try:
            ctl = AilyCtl()
            return ctl.get_llm_model()
        except Exception as e:
            return "N/A"


class ChrLLMKey(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrLLMKey - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMKey - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrLLMKey - onWriteRequest: value = " + str(data))
            data = data.decode("utf-8")

            if data:
                aily = AilyCtl()
                aily.set_llm_key(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMKey - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        try:
            ctl = AilyCtl()
            return ctl.get_llm_key()
        except Exception as e:
            return "N/A"


class ChrLLMPrePrompt(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrLLMPrePrompt - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMPrePrompt - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            data = data.decode("utf-8")
            logger.info("ChrLLMPrePrompt - onWriteRequest: value = " + str(data))

            if data:
                aily = AilyCtl()
                aily.set_llm_preprompt(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMPrePrompt - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        try:
            ctl = AilyCtl()
            return ctl.get_llm_preprompt()
        except Exception as e:
            return "N/A"


class ChrLLMTemp(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrLLMTemp - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMTemp - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            logger.info("ChrLLMTemp - onWriteRequest: value = " + str(data))
            data = data.decode("utf-8")

            if data:
                aily = AilyCtl()
                aily.set_llm_temp(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMTemp - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        try:
            ctl = AilyCtl()
            return ctl.get_llm_temp()
        except Exception as e:
            return "N/A"


class ChrLLMModelOptions(Characteristic):
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
            logger.info("ChrLLMModelOptions - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMModelOptions - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        try:
            # conf_file = os.getenv("AILY_CONFIG_PATH")
            # with open(conf_file, "r") as f:
            #     conf = yaml.safe_load(f)
            # return conf["llm"]["models"]
            config_load = ConfigLoad()
            return config_load.get_llm_models()
        except Exception as e:
            logger.error(f"ChrLLMModelOptions - get_conf: {e}")
            return []

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrLLMModelOptions - onSubscribe")
        self._updateValueCallback = updateValueCallback
        self.start_sending()

    def onUnsubscribe(self):
        logger.info("ChrLLMModelOptions - onUnsubscribe")
        self._updateValueCallback = None
        self.stop_sending()

    def start_sending(self, interval=1):
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
            logger.info("ChrLLMModelOptions - loop_get: value = " + str(records))
            self._value = bytes(json.dumps(records), "utf-8")
            # 判断self._value的长度，如果超过120字节，就分段发送
            for model in records:
                send_data = model["name"] + ":" + model["value"]
                logger.info("model: {0}".format(send_data))
                self._updateValueCallback(send_data.encode("utf-8"))
        else:
            # self._updateValueCallback(bytes(str([]), "utf-8"))
            pass

        self._updateValueCallback(bytes("EOF", "utf-8"))
        self.stop_sending()
