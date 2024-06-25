import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

from utils.aily_ctl import AilyCtl


class ResponseModel(BaseModel):
    status: int = 200
    messages: str = "Success"
    data: any


app = FastAPI()

@app.get("/api/v1/logs")
async def get_logs(
    page: int = 1,
    perPage: int = 10,
):
    aily_ctl = AilyCtl()
    aily_ctl.log_cur_page = page
    res = aily_ctl.get_logs(perPage)
    
    return ResponseModel(data=res)
    

uvicorn.run(app, host="0.0.0.0", port=8888)
