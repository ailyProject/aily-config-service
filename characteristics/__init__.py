from .chr_battery import ChrBattery
from .chr_cpu_tempture import ChrCpuTemperature
from .chr_cpu_usage import ChrCpuUsage
from .chr_device_id import ChrDeviceId
from .chr_disk_usage import ChrDiskUsage
from .chr_ip import ChrIP
from .chr_model import ChrModel
from .chr_network import ChrNetwork
from .chr_power import ChrPower
from .chr_ram_usage import ChrRamUsage

from .chr_wifi_configuration import ChrWifiConfiguration
from .chr_llm_configuration import ChrLLMConfiguration
from .chr_stt_configuration import ChrSTTConfiguration
from .chr_tts_configuration import ChrTTSConfiguration

from .chr_llm_models import ChrLLMModels
from .chr_stt_models import ChrSTTModels
from .chr_tts_models import ChrTTSModels
from .chr_tts_roles import ChrTTSRoles


__all__ = [
    "ChrBattery",
    "ChrCpuTemperature",
    "ChrCpuUsage",
    "ChrDeviceId",
    "ChrDiskUsage",
    "ChrIP",
    "ChrModel",
    "ChrNetwork",
    "ChrPower",
    "ChrRamUsage",
    "ChrWifiConfiguration",
    "ChrLLMConfiguration",
    "ChrSTTConfiguration",
    "ChrTTSConfiguration",
    "ChrLLMModels",
    "ChrSTTModels",
    "ChrTTSModels",
    "ChrTTSRoles",
]
