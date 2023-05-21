import json
from typing import Union, List
# import pandas as pd

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from starlette.middleware.cors import CORSMiddleware
# from pydantic import BaseModel

from dbClass import dbClass
from common import *

app = FastAPI()

cse191db = dbClass()

origins = [
    "https://cse191.ucsd.edu"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["*"],
    max_age=3600,
)


def setHeaders(response: Response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Origin,X-Requested-With,Content-Type,Authorization,Accept'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,GET,PUT,POST,DELETE'
    response.headers['Service'] = 'CSE191-G00-API'
    

@app.get('/', response_class=PlainTextResponse)
def home():
    return 'Group03 API\n'


@app.get('/health')
def process_health(response: Response):
    setHeaders(response)
    return {"resp": "OK"}

@app.get('/list-forecast', response_class=PlainTextResponse)
def process_forecast(response: Response, gn: Union[str, None] = '3foldCord', outtype: Union[str, None] = 'JSON'):
    setHeaders(response)
    forecast_list = cse191db.loadWeather(gn)
    if outtype == "JSON":
        dl_string = forecast_list.to_json(orient="records")
    else:
        dl_string = forecast_list.to_string()
    return dl_string

@app.get('/list-students', response_class=PlainTextResponse)
def process_list_students(response: Response, gn: Union[int, None] = None, outtype: Union[str, None] = None):
    setHeaders(response)
    student_list = cse191db.loadStudents(gn)
    if outtype == "JSON":
        sl_string = student_list.to_json(orient="records")
    else:
        sl_string = student_list.to_string()
    return sl_string

@app.get('/list-devices', response_class=PlainTextResponse)
def process_list_device(response: Response, gn: Union[int, None] = None, outtype: Union[str, None] = None):
    setHeaders(response)
    device_list = cse191db.loadDevices(gn)
    if outtype == "JSON":
        dl_string = device_list.to_json(orient="records")
    else:
        dl_string = device_list.to_string()
    return dl_string

@app.get('/list-ble-logs', response_class=PlainTextResponse)
def process_list_ble_logs(response: Response, gn: Union[int, None] = None, outtype: Union[str, None] = None):
    setHeaders(response)
    ble_log_list = cse191db.loadBleLogs(gn)
    if outtype == "JSON":
        dl_string = ble_log_list.to_json(orient="records")
    else:
        dl_string = ble_log_list.to_string()
    return dl_string


@app.post('/log-devices')
def process_log_device(response: Response, data: LogInfo):
    setHeaders(response)  
    if cse191db.logDevices(data):
        return {"resp": "OK"}
    else:
        return {"resp": "FAIL"}


# run the app
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)