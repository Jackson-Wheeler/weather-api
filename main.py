import json
from typing import Union, List
from time import sleep
import requests

import uvicorn
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from fastapi_utils.tasks import repeat_every
from starlette.middleware.cors import CORSMiddleware

from dbClass import dbClass
from common import *

weather_fetch_delay = 60*60

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
def process_forecast(response: Response, gn: Union[str, None] = None, outtype: Union[str, None] = 'JSON'):
    setHeaders(response)
    forecast_list = cse191db.loadWeather(gn)
    if outtype == "JSON":
        dl_string = forecast_list.to_json(orient="records")
    else:
        dl_string = forecast_list.to_string()
    return dl_string

# Repeated event
@app.on_event("startup")
@repeat_every(seconds=weather_fetch_delay)
def make_api_call():
    make_weather_api_call()


def make_weather_api_call():
    print("Making Weather API Call")
    api_url = "https://api.openweathermap.org/data/2.5/weather?lat=37.5519&units=imperial&lon=126.9918&appid=0354c29c5e773c46d37727c8a0455d58"
    response = requests.get(api_url)
    data_json = response.json()
    print(data_json)
    # attempt to add to db until success
    while not cse191db.add_to_db(data_json):
        print("Adding to DB failed. Waiting 60 seconds then adding again...")
        sleep(60000)
        continue
    print("Sucessfully Added")
    print()


# run the app
if __name__ == '__main__':
    uvicorn.run("main:app", host="localhost", port=8003, reload=True)
