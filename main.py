import sys
import asyncio
import os

from pybleno import Bleno, BlenoPrimaryService
from loguru import logger
from dotenv import load_dotenv, set_key

load_dotenv(".env")

from characteristics import *


os.environ["AILY_CONFIG_PATH"] = os.path.abspath(os.environ.get("AILY_CONFIG_PATH"))


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
                            ChrLLMModel("123e4567-e89b-12d3-a456-426614174002"),
                            ChrNetwork("123e4567-e89b-12d3-a456-426614174003"),
                            ChrIP("123e4567-e89b-12d3-a456-426614174004"),
                            ChrCpuTemperature("123e4567-e89b-12d3-a456-426614174005"),
                            ChrCpuUsage("123e4567-e89b-12d3-a456-426614174006"),
                            ChrRamUsage("123e4567-e89b-12d3-a456-426614174007"),
                            ChrDiskUsage("123e4567-e89b-12d3-a456-426614174008"),
                            ChrBattery("123e4567-e89b-12d3-a456-426614174009"),
                            ChrPower("123e4567-e89b-12d3-a456-426614174010"),
                            ChrWifi("123e4567-e89b-12d3-a456-00805f9b34fb"),
                            ChrLLMKey("123e4567-e89b-12d3-a456-00805f9b34fd"),
                            ChrLLMPrePrompt("123e4567-e89b-12d3-a456-00805f9b34fe"),
                            ChrLLMTemp("123e4567-e89b-12d3-a456-00805f9b34ff"),
                            ChrLLMModelOptions("123e4567-e89b-12d3-a456-00805f9b3500"),
                            ChrSttModel("123e4567-e89b-12d3-a456-00805f9b3501"),
                            ChrSttKey("123e4567-e89b-12d3-a456-00805f9b3502"),
                            ChrSTTModelOptions("123e4567-e89b-12d3-a456-00805f9b3503"),
                            ChrTTSModel("123e4567-e89b-12d3-a456-00805f9b3504"),
                            ChrTTSKey("123e4567-e89b-12d3-a456-00805f9b3505"),
                            ChrTTSRole("123e4567-e89b-12d3-a456-00805f9b3506"),
                            ChrTTSModelOptions("123e4567-e89b-12d3-a456-00805f9b3507"),
                            ChrTTSRoleOptions("123e4567-e89b-12d3-a456-00805f9b3508"),
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
