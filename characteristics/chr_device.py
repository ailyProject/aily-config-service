import uuid
import socket
import psutil
import time
import threading
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
    
    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrDeviceId - onSubscribe")
        self._updateValueCallback = updateValueCallback

        hostname = self.get_mac()
        logger.info("ChrDeviceId - onReadRequest: value = " + hostname)
        self._value = bytes(hostname, "utf8")

        if self._updateValueCallback:
            self._updateValueCallback(self._value)

    def onUnsubscribe(self):
        logger.info("ChrDeviceId - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None

    @staticmethod
    def get_hostname():
        return socket.gethostname()

    @staticmethod
    def get_mac():
        # 获取 MAC 地址
        mac = uuid.getnode()
        # 转换为常见的 MAC 地址格式
        mac_address = "".join(("%012X" % mac)[i : i + 2] for i in range(0, 12, 2))
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
        self._loop = False
        self._updateValueCallback = None
        self._timer = None
        # self._stop_event = threading.Event()

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_battery()
            logger.info("ChrBattery - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrBattery - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrBattery - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrBattery - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()
    
    def start_sending(self, interval=600):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    @staticmethod
    def get_battery():
        try:
            battery = psutil.sensors_battery()
            return battery.percent
        except Exception as e:
            return "N/A"

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        self._value = bytes(str(self.get_battery()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()

        # while not self._stop_event.is_set() and self._loop:
        #     self._value = bytes(str(self.get_battery()), "utf8")
        #     if self._updateValueCallback:
        #         try:
        #             self._updateValueCallback(self._value)
        #         except Exception as e:
        #             logger.error(f"ChrBattery - loop_get: {e}")
        #     time.sleep(20)


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
        self._loop = False
        self._updateValueCallback = None
        self._timer = None

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_disk_usage()
            logger.info("ChrDiskUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrDiskUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrDiskUsage - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrDiskUsage - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()
    
    def start_sending(self, interval=120):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    @staticmethod
    def get_disk_usage():
        try:
            disk_usage = psutil.disk_usage("/").percent
            return disk_usage
        except Exception as e:
            logger.error("ChrDiskUsage - get_disk_usage: {0}".format(e))
            return "N/A"

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        self._value = bytes(str(self.get_disk_usage()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()

        # while not self._stop_event.is_set() and self._loop:
        #     self._value = bytes(str(self.get_disk_usage()), "utf8")
        #     logger.info("DiskUsage: " + str(self._value))
        #     if self._updateValueCallback:
        #         try:
        #             self._updateValueCallback(self._value)
        #         except Exception as e:
        #             logger.error(f"ChrDiskUsage - loop_get: {e}")
        #     time.sleep(20)


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
        self._loop = False
        self._updateValueCallback = None
        self._timer = None

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_power()
            logger.info("ChrPower - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrPower - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrPower - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        # self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrPower - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()
    
    def start_sending(self, interval=300):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    @staticmethod
    def get_power():
        try:
            # TODO: Implement this method
            battery = psutil.sensors_battery()
            return battery.percent
        except Exception as e:
            return "N/A"

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        self._value = bytes(str(self.get_power()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()

        # while not self._stop_event.is_set() and self._loop:
        #     self._value = bytes(str(self.get_power()), "utf8")
        #     if self._updateValueCallback:
        #         try:
        #             self._updateValueCallback(self._value)
        #         except Exception as e:
        #             logger.error(f"ChrPower - loop_get: {e}")
        #     time.sleep(20)


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
        self._loop = False
        self._updateValueCallback = None
        self._timer = None
        # self._stop_event = threading.Event()

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            data = self.get_ram_usage()
            logger.info("ChrRAMUsage - onReadRequest: value = " + str(data))
            self._value = bytes(str(data), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrRAMUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrRamUsage - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrRamUsage - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()
    
    def start_sending(self, interval=10):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    @staticmethod
    def get_ram_usage():
        ram_usage = psutil.virtual_memory().percent
        return ram_usage

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        self._value = bytes(str(self.get_ram_usage()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()

        # while not self._stop_event.is_set() and self._loop:
        #     self._value = bytes(str(self.get_ram_usage()), "utf8")
        #     if self._updateValueCallback:
        #         try:
        #             self._updateValueCallback(self._value)
        #         except Exception as e:
        #             logger.error(f"ChrRamUsage - loop_get: {e}")
        #     time.sleep(10)


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
        self._loop = False
        self._updateValueCallback = None
        self._timer = None
        # self._stop_event = threading.Event()

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            temp = self.get_cpu_tempture()
            logger.info("ChrCpuTemperature - onReadRequest: value = " + str(temp))
            self._value = bytes(str(temp), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrCpuTemperature - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrCpuTemperature - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrCpuTemperature - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()
    
    def start_sending(self, interval=30):
        if self._timer is not None:
            self._timer.cancel()

        self._timer = threading.Timer(interval, self.loop_get)
        self._timer.start()

    def stop_sending(self):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = None

    @staticmethod
    def get_cpu_tempture():
        try:
            with open("/sys/class/thermal/thermal_zone0/temp") as temp_file:
                cpu_temp = temp_file.read()
                return round(float(cpu_temp) / 1000, 2)
        except FileNotFoundError:
            return "N/A"

    def loop_get(self):
        if self._updateValueCallback is None:
            return

        self._value = bytes(str(self.get_cpu_tempture()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()


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
        self._updateValueCallback = None
        self._loop = False

        self._stop_event = threading.Event()

        self._thread = None
        self._timer = None

    def stop(self):
        # self._stop_event.set()
        self._loop = False

    def onReadRequest(self, offset, callback):
        try:
            usage = self.get_cpu_usage()
            logger.info("ChrCpuUsage - onReadRequest: value = " + str(usage))
            self._value = bytes(str(usage), "utf8")
            callback(Characteristic.RESULT_SUCCESS, self._value)
        except Exception as e:
            logger.error(f"ChrCpuUsage - onReadRequest: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR, None)

    def onSubscribe(self, maxValueSize, updateValueCallback):
        logger.info("ChrCpuUsage - onSubscribe")

        self._updateValueCallback = updateValueCallback
        self._loop = True
        self.start_sending()

        # threading.Thread(target=self.loop_get, daemon=True).start()

    def onUnsubscribe(self):
        logger.info("ChrCpuUsage - onUnsubscribe")

        self._loop = False
        self._updateValueCallback = None
        self.stop_sending()

    @staticmethod
    def get_cpu_usage():
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            return cpu_usage
        except Exception as e:
            return "N/A"

    def start_sending(self, interval=15):
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

        self._value = bytes(str(self.get_cpu_usage()), "utf8")
        if self._value:
            self._updateValueCallback(self._value)

        self.start_sending()
