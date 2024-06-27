import uvicorn
import json

from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from typing import Any, Optional

from loguru import logger

load_dotenv()

from utils.aily_ctl import AilyCtl
from utils.config_ctl import ConfigCtl
from utils.device_ctl import DeviceCtl


aily_ctl = AilyCtl()
conf_ctl = ConfigCtl()
device_ctl = DeviceCtl()


class ResponseModel(BaseModel):
    status: int = 200
    message: str = "success"
    data: Any = None


class ModelDataUpdate(BaseModel):
    llmURL: Optional[str] = ""
    llmModel: Optional[str] = ""
    llmKey: Optional[str] = ""
    llmPrePrompt: Optional[str] = ""
    llmTemp: Optional[str] = ""
    sttURL: Optional[str] = ""
    sttModel: Optional[str] = ""
    sttKey: Optional[str] = ""
    ttsURL: Optional[str] = ""
    ttsModel: Optional[str] = ""
    ttsKey: Optional[str] = ""
    ttsRole: Optional[str] = ""


app = FastAPI()

# 配置跨域相关策略
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"


@app.get(f"{API_PREFIX}/ping")
async def get_ping():
    return ResponseModel(data="pong")


@app.get(f"{API_PREFIX}/logs")
async def get_logs(
    page: int = 1,
    perPage: int = 10,
):
    aily_ctl.log_cur_page = page
    res = aily_ctl.get_logs(perPage)
    data = []
    if res:
        for item in res:
            data.append(
                {
                    "role": "user" if item[0] == "tool" else item[0],
                    "msg": (
                        json.loads(item[1])["url"] if item[2] == "image" else item[1]
                    ),
                    "type": item[2] if item[2] else "text",
                }
            )

    return ResponseModel(data={"page": page, "perPage": perPage, "list": data})


@app.get(f"{API_PREFIX}/llmModelOptions")
async def get_llm_model_options():
    return ResponseModel(data=conf_ctl.get_llm_models())


@app.get(f"{API_PREFIX}/sttModelOptions")
async def get_stt_model_options():
    return ResponseModel(data=conf_ctl.get_stt_models())


@app.get(f"{API_PREFIX}/ttsModelOptions")
async def get_tts_model_options():
    return ResponseModel(data=conf_ctl.get_tts_models())


@app.get(f"{API_PREFIX}/modelData")
async def get_model_data():
    return ResponseModel(
        data={
            "llmURL": aily_ctl.get_llm_url(),
            "llmModel": aily_ctl.get_llm_model(),
            "llmKey": aily_ctl.get_llm_key(),
            "llmPrePrompt": aily_ctl.get_llm_preprompt(),
            "llmTemp": aily_ctl.get_llm_temp(),
            "sttURL": aily_ctl.get_stt_url(),
            "sttModel": aily_ctl.get_stt_model(),
            "sttKey": aily_ctl.get_stt_key(),
            "ttsURL": aily_ctl.get_tts_url(),
            "ttsModel": aily_ctl.get_tts_model(),
            "ttsKey": aily_ctl.get_tts_key(),
            "ttsRole": aily_ctl.get_tts_role(),
        }
    )


@app.post(f"{API_PREFIX}/modelData")
async def set_model_data(
    data: ModelDataUpdate,
):
    aily_ctl.set_llm_url(data.llmURL)
    aily_ctl.set_llm_model(data.llmModel)
    aily_ctl.set_llm_key(data.llmKey)
    aily_ctl.set_llm_preprompt(data.llmPrePrompt)
    aily_ctl.set_llm_temp(data.llmTemp)
    aily_ctl.set_stt_url(data.sttURL)
    aily_ctl.set_stt_model(data.sttModel)
    aily_ctl.set_stt_key(data.sttKey)
    aily_ctl.set_tts_url(data.ttsURL)
    aily_ctl.set_tts_model(data.ttsModel)
    aily_ctl.set_tts_key(data.ttsKey)
    aily_ctl.set_tts_role(data.ttsRole)

    aily_ctl.save("reload")

    return ResponseModel()


uvicorn.run(app, host="0.0.0.0", port=8888)
