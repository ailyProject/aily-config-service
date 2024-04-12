import sys

from pybleno import Bleno, BlenoPrimaryService
from loguru import logger

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
                            ChrBattery("123e4567-e89b-12d3-a456-42661417409"),
                            ChrPower("123e4567-e89b-12d3-a456-42661417410"),
                            
                            ChrWifiConfiguration("123e4567-e89b-12d3-a456-b827eb8fa857")
                        ],
                    }
                )
            ]
        )


bleno.on("advertisingStart", onAdvertisingStart)

bleno.start()

logger.info("Hit <ENTER> to disconnect")

if sys.version_info > (3, 0):
    input()
else:
    raw_input()

bleno.stopAdvertising()
bleno.disconnect()

logger.info("terminated.")
sys.exit(1)
