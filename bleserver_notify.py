import asyncio
import json
import os

from typing import Any, Dict
from loguru import logger

from bless import (  # type: ignore
    BlessServer,
    BlessGATTCharacteristic,
    GATTCharacteristicProperties,
    GATTAttributePermissions,
)
from dotenv import load_dotenv, set_key

from utils.device_ctl import DeviceCtl
from utils.aily_ctl import AilyCtl
from utils.config_ctl import ConfigCtl

load_dotenv(".env")

aily_ctl = AilyCtl()
conf_ctl = ConfigCtl()

logger.add(
    "log.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)

SERVICE_UUID = "123e4567-e89b-12d3-a456-426614174000"
DEVICE_ID_UUID = "123e4567-e89b-12d3-a456-426614174001"
BATTERY_UUID = "123e4567-e89b-12d3-a456-426614174009"
DISK_USAGE_UUID = "123e4567-e89b-12d3-a456-426614174008"
POWER_UUID = "123e4567-e89b-12d3-a456-426614174010"
RAM_USAGE_UUID = "123e4567-e89b-12d3-a456-426614174007"
CPU_TEMP_UUID = "123e4567-e89b-12d3-a456-426614174005"
CPU_USAGE_UUID = "123e4567-e89b-12d3-a456-426614174006"
NETWORK_UUID = "123e4567-e89b-12d3-a456-426614174003"
IP_UUID = "123e4567-e89b-12d3-a456-426614174004"
WIFI_UUID = "123e4567-e89b-12d3-a456-00805f9b34fb"
LLM_MODEL_UUID = "123e4567-e89b-12d3-a456-426614174002"
LLM_URL_UUID = "123e4567-e89b-12d3-a456-00805f9b34fc"
LLM_KEY_UUID = "123e4567-e89b-12d3-a456-00805f9b34fd"
LLM_PRE_PROMPT_UUID = "123e4567-e89b-12d3-a456-00805f9b34fe"
LLM_TEMP_UUID = "123e4567-e89b-12d3-a456-00805f9b34ff"
LLM_MODEL_OPTIONS_UUID = "123e4567-e89b-12d3-a456-00805f9b3500"
STT_URL_UUID = "123e4567-e89b-12d3-a456-00805f9b350c"
STT_MODEL_UUID = "123e4567-e89b-12d3-a456-00805f9b3501"
STT_KEY_UUID = "123e4567-e89b-12d3-a456-00805f9b3502"
STT_MODEL_OPTIONS_UUID = "123e4567-e89b-12d3-a456-00805f9b3503"
TTS_URL_UUID = "123e4567-e89b-12d3-a456-00805f9b350d"
TTS_MODEL_UUID = "123e4567-e89b-12d3-a456-00805f9b3504"
TTS_KEY_UUID = "123e4567-e89b-12d3-a456-00805f9b3505"
TTS_ROLE_UUID = "123e4567-e89b-12d3-a456-00805f9b3506"
TTS_MODEL_OPTIONS_UUID = "123e4567-e89b-12d3-a456-00805f9b3507"
TTS_ROLE_OPTIONS_UUID = "123e4567-e89b-12d3-a456-00805f9b3508"
AILY_STATUS_UUID = "123e4567-e89b-12d3-a456-00805f9b350b"
AILY_RELOAD_UUID = "123e4567-e89b-12d3-a456-00805f9b3509"
AILY_CONVERSATION_UUID = "123e4567-e89b-12d3-a456-00805f9b350a"


NOTIFY_CHRS = {
    BATTERY_UUID: DeviceCtl.get_battery,
    DISK_USAGE_UUID: DeviceCtl.get_disk_usage,
    POWER_UUID: DeviceCtl.get_power,
    RAM_USAGE_UUID: DeviceCtl.get_ram_usage,
    CPU_TEMP_UUID: DeviceCtl.get_cpu_tempture,
    CPU_USAGE_UUID: DeviceCtl.get_cpu_usage,
    NETWORK_UUID: DeviceCtl.get_network,
    IP_UUID: DeviceCtl.get_ip,
    LLM_MODEL_UUID: aily_ctl.get_llm_model,
    AILY_CONVERSATION_UUID: aily_ctl.get_logs,
}

READABLE_CHRS = {
    LLM_MODEL_UUID: aily_ctl.get_llm_model,
    LLM_URL_UUID: aily_ctl.get_llm_url,
    LLM_KEY_UUID: aily_ctl.get_llm_key,
    LLM_PRE_PROMPT_UUID: aily_ctl.get_llm_preprompt,
    LLM_TEMP_UUID: aily_ctl.get_llm_temp,
    STT_URL_UUID: aily_ctl.get_stt_url,
    STT_MODEL_UUID: aily_ctl.get_stt_model,
    STT_KEY_UUID: aily_ctl.get_stt_key,
    TTS_URL_UUID: aily_ctl.get_tts_url,
    TTS_MODEL_UUID: aily_ctl.get_tts_model,
    TTS_KEY_UUID: aily_ctl.get_tts_key,
    TTS_ROLE_UUID: aily_ctl.get_tts_role,
}

WRITEABLE_CHRS = {
    WIFI_UUID: DeviceCtl.set_wifi,
    LLM_MODEL_UUID: aily_ctl.set_llm_model,
    LLM_URL_UUID: aily_ctl.set_llm_url,
    LLM_KEY_UUID: aily_ctl.set_llm_key,
    LLM_PRE_PROMPT_UUID: aily_ctl.set_llm_preprompt,
    LLM_TEMP_UUID: aily_ctl.set_llm_temp,
    STT_URL_UUID: aily_ctl.set_stt_url,
    STT_MODEL_UUID: aily_ctl.set_stt_model,
    STT_KEY_UUID: aily_ctl.set_stt_key,
    TTS_URL_UUID: aily_ctl.set_tts_url,
    TTS_MODEL_UUID: aily_ctl.set_tts_model,
    TTS_KEY_UUID: aily_ctl.set_tts_key,
    TTS_ROLE_UUID: aily_ctl.set_tts_role,
    AILY_RELOAD_UUID: aily_ctl.save,
}


def read_request(characteristic: BlessGATTCharacteristic, **kwargs):
    logger.debug("read characteristic: {0}".format(characteristic.uuid))
    func = READABLE_CHRS.get(characteristic.uuid)
    if func is None:
        logger.debug("Characteristic is not readable")
        return characteristic.value
    
    value = func()
    if isinstance(value, str):
        value = value.encode()
    elif isinstance(value, dict):
        value = json.dumps(value).encode()
    else:
        value = str(value).encode()
    
    characteristic.value = value
    logger.debug(f"Char value: {characteristic.value}")
    return characteristic.value


def write_request(characteristic: BlessGATTCharacteristic, value: Any, **kwargs):
    logger.debug("write characteristic: {0}".format(characteristic.uuid))
    func = WRITEABLE_CHRS.get(characteristic.uuid)
    if func is None:
        logger.debug("Characteristic is not writeable")
        return
    
    func(value.decode("utf-8") if value else None)
    
    
    # characteristic.value = value
    # logger.debug(f"Char value set to {characteristic.value}")
    # if characteristic.value == b'\x0f':
    # logger.debug("Nice")
    # trigger.set()


async def notify(server):
    while True:
        if await server.is_connected():
            for key, func in NOTIFY_CHRS.items():
                chr = server.get_characteristic(key)
                chr.value = str(func()).encode()
                server.update_value(SERVICE_UUID, key)

        await asyncio.sleep(3)


async def run(loop):
    # Instantiate the server
    gatt: Dict = {
        SERVICE_UUID: {
            DEVICE_ID_UUID: {
                "Properties": GATTCharacteristicProperties.read,
                "Permissions": GATTAttributePermissions.readable,
                "Value": DeviceCtl.get_deviceid().encode(),
            }, 
            BATTERY_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_battery()).encode(),
            },
            DISK_USAGE_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_disk_usage()).encode(),
            },
            POWER_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_power()).encode(),
            },
            RAM_USAGE_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_ram_usage()).encode(),
            },
            CPU_TEMP_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_cpu_tempture()).encode(),
            },
            CPU_USAGE_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": str(DeviceCtl.get_cpu_usage()).encode(),
            },
            NETWORK_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": "UNKNOWN".encode(),
            },
            IP_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": "UNKNOWN".encode(),
            },
            WIFI_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": "N/A".encode(),
            },
            LLM_MODEL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_llm_model()).encode(),
            },
            LLM_URL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_llm_url()).encode(),
            },
            LLM_KEY_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_llm_key()).encode(),
            },
            LLM_PRE_PROMPT_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_llm_preprompt()).encode(),
            },
            LLM_TEMP_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_llm_temp()).encode(),
            },
            LLM_MODEL_OPTIONS_UUID: {
                "Properties": GATTCharacteristicProperties.read,
                "Permissions": GATTAttributePermissions.readable,
                "Value": json.dumps(conf_ctl.get_llm_models()).encode(),
            },
            STT_URL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_stt_url()).encode(),
            },
            STT_MODEL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_stt_model()).encode(),
            },
            STT_KEY_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": (aily_ctl.get_stt_key()).encode(),
            },
            STT_MODEL_OPTIONS_UUID: {
                "Properties": GATTCharacteristicProperties.read,
                "Permissions": GATTAttributePermissions.readable,
                "Value": json.dumps(conf_ctl.get_stt_models()).encode(),
            },
            TTS_URL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": aily_ctl.get_tts_url().encode(),
            },
            TTS_MODEL_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": aily_ctl.get_tts_model().encode(),
            },
            TTS_KEY_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": aily_ctl.get_tts_key().encode(),
            },
            TTS_ROLE_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": aily_ctl.get_tts_role().encode(),
            },
            TTS_MODEL_OPTIONS_UUID: {
                "Properties": GATTCharacteristicProperties.read,
                "Permissions": GATTAttributePermissions.readable,
                "Value": json.dumps(conf_ctl.get_tts_models()).encode(),
            },
            TTS_ROLE_OPTIONS_UUID: {
                "Properties": GATTCharacteristicProperties.read,
                "Permissions": GATTAttributePermissions.readable,
                "Value": "{}".encode(),
            },
            AILY_STATUS_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": aily_ctl.get_status().encode(),
            },
            AILY_RELOAD_UUID: {
                "Properties": GATTCharacteristicProperties.read
                | GATTCharacteristicProperties.write,
                "Permissions": GATTAttributePermissions.readable
                | GATTAttributePermissions.writeable,
                "Value": "".encode(),
            },
            AILY_CONVERSATION_UUID: {
                "Properties": GATTCharacteristicProperties.notify,
                "Permissions": GATTAttributePermissions.readable,
                "Value": "".encode(),
            },
        }
    }

    server_name = "Aily"

    server = BlessServer(name=server_name, loop=loop, name_overwrite=True)
    server.read_request_func = read_request
    server.write_request_func = write_request

    await server.add_gatt(gatt)
    await server.start()

    logger.debug("Waiting for someone to subscribe")

    try:
        await notify(server)
    except KeyboardInterrupt:
        logger.debug("Keyboard interrupt detected")
    except Exception as e:
        logger.error(f"Bless server error: {e}")
    finally:
        logger.debug("Stopping")
        await server.stop()


loop = asyncio.get_event_loop()
loop.run_until_complete(run(loop))
