import sys
import asyncio

from pybleno import Bleno, BlenoPrimaryService
from loguru import logger
from dotenv import load_dotenv

load_dotenv(".env")

from characteristics import *


logger.add(
    "log.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)

logger.info("Starting the program")

bleno = Bleno()


def onStateChange(state):
    logger.info("on -> stateChange: " + state)

    if state == "poweredOn":
        bleno.startAdvertising("aily", ["123e4567-e89b-12d3-a456-426614174000"])
    else:
        bleno.stopAdvertising()


bleno.on("stateChange", onStateChange)


def onAdvertisingStart(error):
    logger.info("on -> advertisingStart: " + ("error " + error if error else "success"))

    if not error:
        bleno.setServices(
            [
                BlenoPrimaryService(
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174000",
                        "characteristics": [
                            ChrDeviceId("123e4567-e89b-12d3-a456-426614174001"),
                            ChrModel("123e4567-e89b-12d3-a456-426614174002"),
                            ChrNetwork("123e4567-e89b-12d3-a456-426614174003"),
                            ChrIP("123e4567-e89b-12d3-a456-426614174004"),
                            ChrCpuTemperature("123e4567-e89b-12d3-a456-426614174005"),
                            ChrCpuUsage("123e4567-e89b-12d3-a456-426614174006"),
                            ChrRamUsage("123e4567-e89b-12d3-a456-426614174007"),
                            ChrDiskUsage("123e4567-e89b-12d3-a456-426614174008"),
                            ChrBattery("123e4567-e89b-12d3-a456-426614174009"),
                            ChrPower("123e4567-e89b-12d3-a456-426614174010"),
                            ChrWifiConfiguration("123e4567-e89b-12d3-a456-00805f9b34fb"),
                            ChrLLMConfiguration("123e4567-e89b-12d3-a456-00805f9b34fc"),
                            ChrSTTConfiguration("123e4567-e89b-12d3-a456-00805f9b34fd"),
                            ChrTTSConfiguration("123e4567-e89b-12d3-a456-00805f9b34fe"),
                        ],
                    }
                )
            ]
        )


bleno.on("advertisingStart", onAdvertisingStart)

bleno.start()

try:
    loop = asyncio.get_event_loop()
    loop.run_forever()
except KeyboardInterrupt:
    logger.info("Keyboard interrupt detected")

bleno.stopAdvertising()
bleno.disconnect()

logger.info("terminated.")
sys.exit(1)
