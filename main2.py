import os

from bluezero import peripheral
from bluezero import adapter
from bluezero import async_tools, localGATT
from loguru import logger
from dotenv import load_dotenv

from characteristics import *

load_dotenv(".env")

if os.environ.get("AILY_CONFIG_PATH"):
    os.environ["AILY_CONFIG_PATH"] = os.path.abspath(os.environ.get("AILY_CONFIG_PATH"))

logger.add(
    "aily.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="10 MB",
    compression="zip",
)


def main(adapter_address):
    aily = peripheral.Peripheral(adapter_address=adapter_address, local_name='Aily', appearance=1344)
    aily.add_service(srv_id=1, uuid='123e4567-e89b-12d3-a456-426614174000', primary=True)
    
    # characteristics
    chr_device_id = ChrDeviceId(),
    chr_llm_model = ChrLLMModel(),
    chr_network = ChrNetwork(),
    chr_ip = ChrIP()
    chr_cpu_temp = ChrCpuTemperature()
    chr_cpu_usage = ChrCpuUsage()
    chr_ram_usage = ChrRamUsage()
    chr_disk_usage = ChrDiskUsage()
    chr_battery = ChrBattery()
    chr_power = ChrPower()
    chr_wifi = ChrWifi()
    chr_llm_url = ChrLLMUrl()
    chr_llm_key = ChrLLMKey()
    chr_llm_pre_prompt = ChrLLMPrePrompt()
    chr_llm_temp = ChrLLMTemp()
    chr_llm_model_options = ChrLLMModelOptions()
    chr_stt_url = ChrSTTUrl()
    chr_stt_model = ChrSTTModel()
    chr_stt_key = ChrSTTKey()
    chr_stt_model_options = ChrSTTModelOptions()
    chr_tts_url = ChrTTSUrl()
    chr_tts_model = ChrTTSModel()
    chr_tts_key = ChrTTSKey()
    chr_tts_role = ChrTTSRole()
    chr_tts_model_options = ChrTTSModelOptions()
    chr_tts_role_options = ChrTTSRoleOptions()
    chr_aily_status = ChrAilyStatus()
    chr_aily_reload = ChrAilyReload(aily_status=chr_aily_status)
    chr_aily_convesation = ChrAilyConversation()
    
    aily.add_characteristic(
        srv_id=1, chr_id=1, uuid='123e4567-e89b-12d3-a456-426614174001', 
        value=[], notifying=False, flags=['read', 'notify'], 
        read_callback=chr_wifi.read_callback, 
        write_callback=chr_wifi.write_callback,
        notify_callback=chr_wifi.notify_callback
    )