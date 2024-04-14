import json
import os
from pybleno import Characteristic
from loguru import logger


class ChrWifiConfiguration(Characteristic):
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
            logger.info(
                "ChrWifiConfiguration - onReadRequest: value = " + str(self._value)
            )
            callback(Characteristic.RESULT_SUCCESS, bytes(self._value))
        except Exception as e:
            logger.error(f"ChrWifiConfiguration - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            logger.info(
                "ChrWifiConfiguration - onWriteRequest: value = "
                + self._value.decode("utf-8")
            )
            data = json.loads(self._value.decode("utf-8"))
            result = self.connect(data["ap"], data["password"])
            if result:
                callback(Characteristic.RESULT_SUCCESS)
            else:
                callback(Characteristic.RESULT_UNLIKELY_ERROR)
        except Exception as e:
            logger.error(f"ChrWifiConfiguration - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)

    @staticmethod
    def connect(ssid, password):
        config_lines = [
            "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev",
            "update_config=1",
            "p2p_disabled=1" "\n",
            "network={",
            '\tssid="{}"'.format(ssid),
            '\tpsk="{}"'.format(password),
            "}",
        ]
        config = "\n".join(config_lines)

        # give access and writing. may have to do this manually beforehand
        os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

        # writing to file
        with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
            wifi.write(config)

        logger.info("Wifi config added. Refreshing configs")
        ## refresh configs
        os.popen("sudo wpa_cli -i wlan0 reconfigure")
