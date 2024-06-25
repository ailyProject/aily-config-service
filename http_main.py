import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

from loguru import logger

from utils.aily_ctl import AilyCtl


aily_ctl = AilyCtl()

class ResponseModel(BaseModel):
    code: int = 200
    message: str = "success"
    data: Any = None


app = FastAPI()


@app.get("/api/v1/logs")
async def get_logs(
    page: int = 1,
    perPage: int = 10,
):
    logger.debug(f"get_logs: page={page}, perPage={perPage}")
    aily_ctl.log_cur_page = page
    res = aily_ctl.get_logs(perPage)

    return ResponseModel(data={"page": page, "perPage": perPage, "list": res})


uvicorn.run(app, host="0.0.0.0", port=8888)
