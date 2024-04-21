import psutil
import socket
import array
import os
import json

from pybleno import Characteristic
from loguru import logger
import re
import subprocess


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
        self._updateValueCallback = None

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_network()
            logger.info("ChrNetwork - onReadRequest: value = " + str(data))
            self._value = bytes(data, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrNetwork - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info('EchoCharacteristic - onSubscribe')
        
        self._updateValueCallback = updateValueCallback
        
        self.emit_update()

    def onUnsubscribe(self):
        logger.info('EchoCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None
    
    def emit_update(self):
        try:
            if self._updateValueCallback:
                self._value = bytes(self.get_network(), "utf-8")
                self._updateValueCallback(self._value)
        except Exception as e:
            logger.error("emitUpdateError: {0}".format(e))

    @staticmethod
    def get_network():
        net_status_list = psutil.net_if_stats()
        # 当前网络接口
        current_net = None
        for key, value in net_status_list.items():
            if re.match(r"^lo", key):
                continue
            if value.isup:
                current_net = key

        if current_net is None:
            return "None"
        elif re.match(r"^wlan", current_net):
            return "WiFi"
        elif re.match(r"^eth", current_net):
            return "Wired"
        else:
            return "UNKNOWN"


class ChrIP(Characteristic):
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
        self._updateValueCallback = None

    @staticmethod
    def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(("10.255.255.255", 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = "UNKNOWN"
        finally:
            s.close()
        return IP

    def onReadRequest(self, offset, callback):
        try:
            ip_address = self.get_ip()
            logger.info("ChrIP - onReadRequest: value = " + str(ip_address))
            # 获取当前ip地址
            self._value = bytes(ip_address, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrIP - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info('EchoCharacteristic - onSubscribe')
        
        self._updateValueCallback = updateValueCallback
        
        self.emit_update()

    def onUnsubscribe(self):
        logger.info('EchoCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None
    
    def emit_update(self):
        try:
            if self._updateValueCallback:
                self._value = bytes(self.get_ip(), "utf-8")
                self._updateValueCallback(self._value)
        except Exception as e:
            logger.error("emitUpdateError: {0}".format(e))


class ChrWifi(Characteristic):
    def __init__(self, uuid, chr_ip, chr_network):
        Characteristic.__init__(
            self,
            {
                "uuid": uuid,
                "properties": ["read", "write", "notify"],
                "value": None,
            },
        )
        self._value = None
        self._updateValueCallback = None
        
        self.chr_ip = chr_ip
        self.chr_network = chr_network

    def onReadRequest(self, offset, callback):
        try:
            logger.info(
                "ChrWifi - onReadRequest: value = " + str(self._value)
            )
            callback(Characteristic.RESULT_SUCCESS, bytes(self._value if self._value else ""))
        except Exception as e:
            logger.error(f"ChrWifi - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            self._value = data
            logger.info(
                "ChrWifi - onWriteRequest: value = "
                + self._value.decode("utf-8")
            )
            data = json.loads(self._value.decode("utf-8"))
            result = self.connect(data["ssid"], data["password"])
            if result:
                ChrIP.emit_update()
                ChrNetwork.emit_update()
                callback(Characteristic.RESULT_SUCCESS)
            else:
                callback(Characteristic.RESULT_UNLIKELY_ERROR)
        except Exception as e:
            logger.error(f"ChrWifi - onWriteRequest: {e}")
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
        subprocess.check_call(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
        return True
