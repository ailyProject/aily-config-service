import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any

from utils.aily_ctl import AilyCtl


class ResponseModel(BaseModel):
    code: int
    message: str
    data: Any = None


app = FastAPI()


@app.get("/api/v1/logs")
async def get_logs(
    page: int = 1,
    perPage: int = 10,
):
    aily_ctl = AilyCtl()
    aily_ctl.log_cur_page = page
    res = aily_ctl.get_logs(perPage)

    return ResponseModel(data={"page": page, "perPage": perPage, "list": res})


uvicorn.run(app, host="0.0.0.0", port=8888)
