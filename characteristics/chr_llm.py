import os
import json
import yaml
from pybleno import Characteristic
from loguru import logger
from aily import AilyCtl


class ChrLLMModel(Characteristic):
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
            data = self.get_llm_model()
            logger.info("ChrLLMModel - onReadRequest: value = " + str(data))
            # 获取当前ip地址
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMModel - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrLLMModel - onWriteRequest: value = " + str(data))

            if data:
                aily = AilyCtl()
                aily.set_llm_model(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMModel - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        ctl = AilyCtl()
        return ctl.get_llm_model()


class ChrLLMKey(Characteristic):
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
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrLLMKey - onWriteRequest: value = " + str(data))

            if data:
                aily = AilyCtl()
                aily.set_llm_key(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMKey - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        ctl = AilyCtl()
        return ctl.get_llm_key()


class ChrLLMPrePrompt(Characteristic):
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
            data = json.loads(data.decode("utf-8"))
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
        ctl = AilyCtl()
        return ctl.get_llm_preprompt()


class ChrLLMTemp(Characteristic):
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
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrLLMTemp - onWriteRequest: value = " + str(data))

            if data:
                aily = AilyCtl()
                aily.set_llm_preprompt(data)

            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrLLMTemp - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def get_llm_model():
        ctl = AilyCtl()
        return ctl.get_llm_temp()


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

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_conf()
            logger.info("ChrLLMModels - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrLLMModels - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_conf():
        conf_file = os.getenv("AILY_CONFIG_PATH")
        with open(conf_file, "r") as f:
            conf = yaml.safe_load(f)
        return json.dumps(conf["llm"]["models"])
