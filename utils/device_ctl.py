import uuid
import psutil
import socket
import re
import os
import asyncio
import subprocess
import json
from loguru import logger


class DeviceCtl:
    def __init__(self):
        pass
    
    @staticmethod
    def get_deviceid():
        # 获取 MAC 地址
        mac = uuid.getnode()
        # 转换为常见的 MAC 地址格式
        mac_address = "".join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))
        return mac_address
    
    @staticmethod
    def get_battery():
        try:
            battery = psutil.sensors_battery()
            return battery.percent
        except Exception as e:
            return "N/A"

    @staticmethod
    def get_disk_usage():
        try:
            disk_usage = psutil.disk_usage("/").percent
            return disk_usage
        except Exception as e:
            logger.error("ChrDiskUsage - get_disk_usage: {0}".format(e))
            return "N/A"

    @staticmethod
    def get_power():
        try:
            # TODO: Implement this method
            battery = psutil.sensors_battery()
            return battery.percent
        except Exception as e:
            return "N/A"
    
    @staticmethod
    def get_ram_usage():
        try:
            ram_usage = psutil.virtual_memory().percent
            return ram_usage
        except Exception as e:
            return "N/A"
    
    @staticmethod
    def get_cpu_tempture():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
                cpu_temp = temp_file.read()
                return round(float(cpu_temp) / 1000, 2)
        except FileNotFoundError:
            return "N/A"
    
    @staticmethod
    def get_cpu_usage():
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage
        except Exception as e:
            return "N/A"
    
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
    
    def _scan_wifi(self):
        try:
            subprocess.check_output(["sudo", "nmcli", "dev", "wifi", "rescan"])
        except Exception as e:
            logger.error("Failed to scan wifi: {0}".format(e))
            return "N/A"
    
    def set_wifi(self, value: str):
        data = json.loads(value)
        if not data:
            return
        
        ssid = data.get("ssid")
        password = data.get("password")
        if not ssid or not password:
            return
        
        retry = 5
        find = False

        while retry > 0:
            self._scan_wifi()
            
            result = subprocess.check_output(["sudo", "nmcli", "dev", "wifi", "list"])
            # logger.debug("Wifi list: {0}".format(result.decode("utf-8")))
            ssid_list = result.decode("utf-8").split("\n")[1:]
            ssid_list = [ssid.split()[1] for ssid in ssid_list if ssid]
            
            if ssid in ssid_list:
                find = True
                break

            retry -= 1
        
        if not find:
            logger.error("SSID: {0} not found".format(ssid))
            return -1

        result = subprocess.check_output(["sudo", "nmcli", "device", "wifi", "connect", ssid, "password", password])
        if "successfully activated" in result.decode("utf-8"):
            return 1
        else:
            logger.debug("Failed to connect to {0}".format(ssid))
            return -2

        # config_lines = [
        #     "ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev",
        #     "update_config=1",
        #     "p2p_disabled=1" "\n",
        #     "network={",
        #     '\tssid="{}"'.format(ssid),
        #     '\tpsk="{}"'.format(password),
        #     "}",
        # ]
        # config = "\n".join(config_lines)

        # # give access and writing. may have to do this manually beforehand
        # os.popen("sudo chmod a+w /etc/wpa_supplicant/wpa_supplicant.conf")

        # # writing to file
        # with open("/etc/wpa_supplicant/wpa_supplicant.conf", "w") as wifi:
        #     wifi.write(config)

        # logger.info("Wifi config added. Refreshing configs")
        # ## refresh configs
        # subprocess.check_call(["sudo", "wpa_cli", "-i", "wlan0", "reconfigure"])
        