import uuid
import socket
import psutil
from pybleno import Characteristic
from loguru import logger


class ChrDeviceId(Characteristic):
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
            hostname = self.get_mac()
            logger.info("ChrDeviceId - onReadRequest: value = " + hostname)
            self._value = bytes(hostname, "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrDeviceId - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_mac():
        # 获取 MAC 地址
        mac = uuid.getnode()
        # 转换为常见的 MAC 地址格式
        mac_address = ''.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))
        return mac_address


class ChrBattery(Characteristic):
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
            data = self.get_battery()
            logger.info("ChrBattery - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrBattery - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_battery():
        battery = psutil.sensors_battery()
        return battery.percent


class ChrDiskUsage(Characteristic):
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
            data = self.get_disk_usage()
            logger.info("ChrDiskUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrDiskUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_disk_usage():
        disk_usage = psutil.disk_usage("/").percent
        return disk_usage


class ChrPower(Characteristic):
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
            data = self.get_power()
            logger.info("ChrPower - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrPower - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_power():
        # TODO: Implement this method
        battery = psutil.sensors_battery()
        return battery.percent


class ChrRamUsage(Characteristic):
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
            data = self.get_ram_usage()
            logger.info("ChrRAMUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrRAMUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_ram_usage():
        ram_usage = psutil.virtual_memory().percent
        return ram_usage


class ChrCpuTemperature(Characteristic):
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
            temp = self.get_cpu_tempture()
            logger.info("temp: {0}".format(temp))
            logger.info("ChrCpuTemperature - onReadRequest: value = " + str(temp))
            self._value = bytes(str(temp), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrCpuTemperature - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_cpu_tempture():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
                cpu_temp = temp_file.read()
                return round(float(cpu_temp) / 1000, 2)
        except FileNotFoundError:
            return "N/A"


class ChrCpuUsage(Characteristic):
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
            usage = self.get_cpu_usage()
            logger.info("ChrCpuUsage - onReadRequest: value = " + str(usage))
            self._value = bytes(str(usage), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrCpuUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    @staticmethod
    def get_cpu_usage():
        cpu_usage = psutil.cpu_percent(interval=1)
        return cpu_usage