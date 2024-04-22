import json
import os
import yaml
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
            data = json.loads(data.decode("utf-8"))
            logger.info("ChrTTSModel - onWriteRequest: value = " + str(data))

            aily = AilyCtl()
            aily.set_stt_model(data)

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
            data = json.loads(data.decode("utf-8"))
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
            data = json.loads(data.decode("utf-8"))
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

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_conf()
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
            return json.dumps(conf["tts"]["models"])
        except Exception as e:
            return "N/A"


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

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_conf()
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
            return json.dumps(conf["tts"]["roles"])
        except Exception as e:
            return "N/A"