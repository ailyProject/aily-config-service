import psutil
import socket
import array
import os
import json
import time

from pybleno import Characteristic
from loguru import logger
import re
import subprocess
import threading


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
        
        # self.emit_update()

    def onUnsubscribe(self):
        logger.info('EchoCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None
    
    def emit_update(self):
        try:
            if self._updateValueCallback:
                # value = self.get_network()
                while_count = 5
                while while_count > 0:
                    value = self.get_network()
                    if value != "UNKNOWN":
                        break
                    time.sleep(2)
                    while_count -= 1

                logger.info("ChrNetwork - emit_update: {0}".format(value))
                self._value = bytes(value, "utf-8")
                self._updateValueCallback(self._value)
        except Exception as e:
            logger.error("emitUpdateError: {0}".format(e))

    @staticmethod
    def get_network():
        net_status_list = psutil.net_if_stats()
        # 当前网络接口
        
        current_net = "UNKNOWN"
        for key, value in net_status_list.items():
            if re.match(r"^lo", key):
                continue
            if value.isup:
                current_net = key

        if re.match(r"^wlan", current_net):
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
        
        # self.emit_update()

    def onUnsubscribe(self):
        logger.info('EchoCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None
    
    def emit_update(self):
        try:
            if self._updateValueCallback:
                while_count = 5
                while while_count > 0:
                    value = self.get_ip()
                    if value != "UNKNOWN" and value != self._value.decode("utf-8"):
                        break
                    time.sleep(5)
                    while_count -= 1
                logger.info("ChrIP - emit_update: {0}".format(value))
                self._value = bytes(value, "utf-8")
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
            t = threading.Thread(
                target=self.connect, args=(data["ssid"], data["password"])
            )
            t.start()
            callback(Characteristic.RESULT_SUCCESS)
        except Exception as e:
            logger.error(f"ChrWifi - onWriteRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
    
    def emit_update(self):
        time.sleep(5)
        self.chr_ip.emit_update()
        self.chr_network.emit_update()

    def connect(self, ssid, password):
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
        self.emit_update()
        return True
