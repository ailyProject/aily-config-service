from .chr_device import (
    ChrBattery,
    ChrCpuTemperature,
    ChrCpuUsage,
    ChrDeviceId,
    ChrDiskUsage,
    ChrPower,
    ChrRamUsage,
)
from .chr_network import ChrIP, ChrNetwork, ChrWifi
from .chr_llm import (
    ChrLLMModel,
    ChrLLMKey,
    ChrLLMPrePrompt,
    ChrLLMTemp,
    ChrLLMModelOptions,
)
from .chr_stt import ChrSTTModel, ChrSTTKey, ChrSTTModelOptions
from .chr_tts import (
    ChrTTSModel,
    ChrTTSKey,
    ChrTTSRole,
    ChrTTSModelOptions,
    ChrTTSRoleOptions,
)
from .chr_aily import ChrAilyReload, ChrAilyConversation, ChrAilyStatus


__all__ = [
    "ChrBattery",
    "ChrCpuTemperature",
    "ChrCpuUsage",
    "ChrDeviceId",
    "ChrDiskUsage",
    "ChrPower",
    "ChrRamUsage",
    "ChrIP",
    "ChrNetwork",
    "ChrWifi",
    "ChrLLMModel",
    "ChrLLMKey",
    "ChrLLMPrePrompt",
    "ChrLLMTemp",
    "ChrLLMModelOptions",
    "ChrSTTModel",
    "ChrSTTKey",
    "ChrSTTModelOptions",
    "ChrTTSModel",
    "ChrTTSKey",
    "ChrTTSRole",
    "ChrTTSModelOptions",
    "ChrTTSRoleOptions",
    "ChrAilyReload",
    "ChrAilyConversation",
    "ChrAilyStatus"
]
