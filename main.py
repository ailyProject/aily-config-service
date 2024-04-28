import sys
import asyncio
import os

from pybleno import Bleno, BlenoPrimaryService
from loguru import logger
from dotenv import load_dotenv, set_key

load_dotenv(".env")

from characteristics import *


if os.environ.get("AILY_CONFIG_PATH"):
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

chr_device_id = ChrDeviceId("123e4567-e89b-12d3-a456-426614174001")
chr_llm_model = ChrLLMModel("123e4567-e89b-12d3-a456-426614174002")
chr_network = ChrNetwork("123e4567-e89b-12d3-a456-426614174003")
chr_ip = ChrIP("123e4567-e89b-12d3-a456-426614174004")
chr_cpu_temp = ChrCpuTemperature("123e4567-e89b-12d3-a456-426614174005")
chr_cpu_usage = ChrCpuUsage("123e4567-e89b-12d3-a456-426614174006")
chr_ram_usage = ChrRamUsage("123e4567-e89b-12d3-a456-426614174007")
chr_disk_usage = ChrDiskUsage("123e4567-e89b-12d3-a456-426614174008")
chr_battery = ChrBattery("123e4567-e89b-12d3-a456-426614174009")
chr_power = ChrPower("123e4567-e89b-12d3-a456-426614174010")
chr_wifi = ChrWifi(
    "123e4567-e89b-12d3-a456-00805f9b34fb", chr_ip=chr_ip, chr_network=chr_network
)
chr_llm_key = ChrLLMKey("123e4567-e89b-12d3-a456-00805f9b34fd")
chr_llm_pre_prompt = ChrLLMPrePrompt("123e4567-e89b-12d3-a456-00805f9b34fe")
chr_llm_temp = ChrLLMTemp("123e4567-e89b-12d3-a456-00805f9b34ff")
chr_llm_model_options = ChrLLMModelOptions("123e4567-e89b-12d3-a456-00805f9b3500")
chr_stt_model = ChrSTTModel("123e4567-e89b-12d3-a456-00805f9b3501")
chr_stt_key = ChrSTTKey("123e4567-e89b-12d3-a456-00805f9b3502")
chr_stt_model_options = ChrSTTModelOptions("123e4567-e89b-12d3-a456-00805f9b3503")
chr_tts_model = ChrTTSModel("123e4567-e89b-12d3-a456-00805f9b3504")
chr_tts_key = ChrTTSKey("123e4567-e89b-12d3-a456-00805f9b3505")
chr_tts_role = ChrTTSRole("123e4567-e89b-12d3-a456-00805f9b3506")
chr_tts_model_options = ChrTTSModelOptions("123e4567-e89b-12d3-a456-00805f9b3507")
chr_tts_role_options = ChrTTSRoleOptions("123e4567-e89b-12d3-a456-00805f9b3508")
chr_aily_status = ChrAilyStatus("123e4567-e89b-12d3-a456-00805f9b350b")
chr_aily_reload = ChrAilyReload("123e4567-e89b-12d3-a456-00805f9b3509", aily_status=chr_aily_status)
chr_aily_convesation = ChrAilyConversation("123e4567-e89b-12d3-a456-00805f9b350a")


def onAdvertisingStart(error):
    logger.info("on -> advertisingStart: " + ("error " + error if error else "success"))

    if not error:
        bleno.setServices(
            [
                BlenoPrimaryService(
                    {
                        "uuid": "123e4567-e89b-12d3-a456-426614174000",
                        "characteristics": [
                            chr_device_id,
                            chr_llm_model,
                            chr_network,
                            chr_ip,
                            chr_cpu_temp,
                            chr_cpu_usage,
                            chr_ram_usage,
                            chr_disk_usage,
                            chr_battery,
                            chr_power,
                            chr_wifi,
                            chr_llm_key,
                            chr_llm_pre_prompt,
                            chr_llm_temp,
                            chr_llm_model_options,
                            chr_stt_model,
                            chr_stt_key,
                            chr_stt_model_options,
                            chr_tts_model,
                            chr_tts_key,
                            chr_tts_role,
                            chr_tts_model_options,
                            chr_tts_role_options,
                            chr_aily_reload,
                            chr_aily_convesation,
                            chr_aily_status,
                        ],
                    }
                )
            ]
        )


bleno.on("advertisingStart", onAdvertisingStart)


try:
    bleno.start()
    input("Press <Enter> to stop the program\n")
except KeyboardInterrupt:
    logger.info("Keyboard interrupt detected")
except Exception as e:
    logger.error(f"Bleno service error: {e}")
finally:
    bleno.stopAdvertising()
    bleno.disconnect()
    chr_cpu_usage.stop()
    chr_cpu_temp.stop()
    chr_ram_usage.stop()
    chr_disk_usage.stop()
    chr_battery.stop()
    chr_power.stop()

    logger.info("terminated.")
    sys.exit(1)
