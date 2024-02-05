import pandas as pd
import time
import traceback
from datetime import datetime
import logging
import json
from finta import TA
# from wrappers import retry
import ccxt
import uuid
import requests
from functools import wraps
import certifi



#CONFIGURATIONS
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
data={}
with open("datamanagement/helpful_scripts/background.json") as json_file:
    data=json.load(json_file)
client = MongoClient(data['mongo_uri'], server_api=ServerApi('1'),connect=False,tlsCAFile=certifi.where())
database=client[data['database']]
admin=database['admin']
position=database['position']
order_logs=database['order_logs']

print(type(admin.find()))
if(len(list(admin.find()))<1):
    admin.insert_one({
        "name":"jonasberes",
        "password":"aDamko^95",
        "client_id":2493,
        "secret_key":"84226cf9-a8ed-41f9-999f-c44b8afa99ed",
        "breakout_lines":[10,20],
        "breakout_tolerance":8,
        "wick_tolerance":50,
        "risk_per_trade":100,
        "max_candle_body_size":20,
        "stop_loss_historical_candles":6,
        "stop_loss_wg_room":2,
        "symbols":["MNQ","MES"],
        "status":True,
        "live":False,
        "time_frame":"5m"
    })

params={
    "name":"jonasberes",
    "password":"aDamko^95",
    "client_id":2493,
    "secret_key":"84226cf9-a8ed-41f9-999f-c44b8afa99ed",
    "breakout_lines":{
        "MNQ":[10,20],
        "MES":[10,20]
    },
    "breakout_tolerance":8,
    "wick_tolerance":50,
    "risk_per_trade":100,
    "max_candle_body_size":20,
    "stop_loss_historical_candles":6,
    "stop_loss_wg_room":2,
    "symbols":["MNQ","MES"],
    "status":True,
    "live":False,
    "time_frame":"5m"
}

admin.update_one({},{"$set":params})