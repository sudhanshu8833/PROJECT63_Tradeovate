import pandas as pd
import time
import traceback
from datetime import datetime
import logging
import json
from finta import TA
import certifi
import pytz
# from wrappers import retry
from datamanagement.helpful_scripts.wrappers import retry
import uuid
import requests
import yfinance as yf
from functools import wraps

from datamanagement.models import *
from datamanagement.helpful_scripts.wrappers import *



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


'''
# ADMIN
{
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

# POSITION
{
    "symbol":"",
    "status": OPEN | CLOSED,
    "type": LONG | SHORT,
    "time_start":"",
    "time_end":"",
    "quantity":"",
    "pnl":"",
    "current_price":"",
    "price_in":"",
    "price_out":"",
    "stoploss":"",
    "take_profit":""
}
'''

class run_strategy():

    def __init__(self):
        self.ltp_prices={}
        self.times=time.time()
        self.admin=admin.find_one()

        self.debug=True
        if(self.admin['live']==True):
            self.base_url="https://live.tradovateapi.com/"
        else:
            self.base_url="https://demo.tradovateapi.com/"
        self.login()
        self.positions={}
        self.retries=3
        self.prices={}




    @retry(times=3)
    def login(self):
        url=self.base_url+"v1/auth/accesstokenrequest"

        headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }

        data = {
            "name": self.admin['name'],
            "password": self.admin['password'],
            "appId": "jonasberes",
            "appVersion": "0.0.1",
            "cid": self.admin['client_id'],
            "sec": self.admin['secret_key'],
            "deviceId":str(uuid.uuid4())
        }

        response = requests.post(url, headers=headers, json=data)
        self.token=response.json()['accessToken']


    def download_ohlc(self,instrument):
        df=yf.download(instrument+"=F",interval=self.admin['time_frame'],period='1d')
        self.prices[instrument]=df['Close'].iloc[-1]
        return df[:-1]


    def create_order(self,params):
        pass


    def close_trade(self,params):
        pass

    def buy_signal(self,instrument,df):
        high=self.admin['breakout_lines'][instrument][1]
        low=self.admin['breakout_lines'][instrument][0]
        price=df['Close'].iloc[-1]
        stoploss="NA"
        takeprofit="NA"
        type="NA"
        quantity="NA"

        if(price>=high):
            wick=float(df['High'].iloc[-1]-df['Close'].iloc[-1])
            body_above=float(df['Close'].iloc[-1]-high)
            percentage_wick=(wick/(body_above+wick))*100

            if(price-high>=self.admin['breakout_tolerance']):

                if(percentage_wick<=self.admin['wick_tolerance']):

                    candle_body_size=df['Close'].iloc[-1]-df['Open'].iloc[-1]
                    if(candle_body_size<=self.admin['max_candle_body_size']):
                        lookback=-1*self.admin['stop_loss_historical_candles']
                        stoploss=df['Close'][lookback:].max()-self.admin['stop_loss_wg_room']
                        takeprofit=price+(price-stoploss)
                        quantity=(self.admin['risk_per_trade']/(price-stoploss))
                        type="LONG"


                    else:
                        takeprofit=high-self.admin['stop_loss_wg_room']
                        stoploss=price+(price-takeprofit)
                        quantity=int(self.admin['risk_per_trade']/(price-stoploss))
                        type="SHORT"
                else:
                    stoploss=df['High'].iloc[-1]+self.admin['stop_loss_wg_room']
                    takeprofit=price-(stoploss-price)
                    quantity=int(self.admin['risk_per_trade']/(price-stoploss))
                    type="SHORT"


        if(stoploss!="NA"):
            params={
                "price_in":price,
                "type":type,
                "symbol":instrument,
                "status":"OPEN",
                "time_start":datetime.now(),
                "time_end":datetime.now(),
                "quantity":quantity,
                "price_out":0,
                "stoploss":stoploss,
                "take_profit":takeprofit,
                "current_price":price,
                "pnl":0
            }
            if(self.admin['live']):
                self.create_order(params)
            position.insert_one(params)
            return params

        return "NA"


    def sell_signal(self,instrument,df):
        high=self.admin['breakout_lines'][instrument][1]
        low=self.admin['breakout_lines'][instrument][0]
        price=df['Close'].iloc[-1]
        stoploss="NA"
        takeprofit="NA"
        type="NA"
        quantity="NA"

        if(price<=low):
            wick=float(df['Close'].iloc[-1]-df['Low'].iloc[-1])
            body_below=float(low-df['Close'].iloc[-1])
            percentage_wick=(wick/(body_below+wick))*100

            if(low-price>=self.admin['breakout_tolerance']):
                    
                if(percentage_wick<=self.admin['wick_tolerance']):

                    candle_body_size=df['Open'].iloc[-1]-df['Close'].iloc[-1]
                    if(candle_body_size<=self.admin['max_candle_body_size']):
                        lookback=-1*self.admin['stop_loss_historical_candles']
                        stoploss=df['Close'][lookback:].min()+self.admin['stop_loss_wg_room']
                        takeprofit=price-(stoploss-price)
                        quantity=(self.admin['risk_per_trade']/(stoploss-price))
                    else:
                        takeprofit=low+self.admin['stop_loss_wg_room']
                        stoploss=price-(takeprofit-price)
                        quantity=int(self.admin['risk_per_trade']/(price-stoploss))
                        type="LONG"
                else:
                    stoploss=df['Low'].iloc[-1]-self.admin['stop_loss_wg_room']
                    takeprofit=price+(price-stoploss)
                    quantity=int(self.admin['risk_per_trade']/(price-stoploss))
                    type="LONG"

        if(stoploss!="NA"):
            params={
                "price_in":price,
                "type":type,
                "symbol":instrument,
                "status":"OPEN",
                "time_start":datetime.now(),
                "time_end":datetime.now(),
                "quantity":quantity,
                "price_out":0,
                "stoploss":stoploss,
                "take_profit":takeprofit,
                "current_price":price,
                "pnl":0
            }
            if(self.admin['live']):
                self.create_order(params)
            position.insert_one(params)
            return params

        return "NA"

    def signals(self,instrument,df):
        if(instrument not in self.positions or self.positions[instrument]==False):
            time_now=datetime.now(tz=pytz.timezone(data['timezone']))
            if (time_now.hour==10 and time_now.minute>=10 and time_now.minute<=30) or self.debug:
                buy_signal=self.buy_signal(instrument,df)
                if(buy_signal!="NA"):
                    self.positions[instrument]=True
                    if(buy_signal['type']=="SHORT"):
                        return "sell"
                    return 'buy'


                sell_signal=self.sell_signal(instrument,df)
                if(sell_signal!="NA"):
                    self.positions[instrument]=True
                    if(sell_signal['type']=="LONG"):
                        return "buy"
                    return 'sell'

        return "NA"

    def update_ltp(self):
        pass

    def close_signal(self):
        positions=position.find()
        self.update_ltp()

        for pos in positions:
            if(pos['status']=="OPEN"):
                pos['current_price']=self.prices[pos['symbol']]
                if(pos['type']=='LONG'):
                    pos['pnl']=round(pos['current_price']-pos['price_in'],2)
                    if(pos['current_price']>=pos['take_profit'] or pos['current_price']<=pos['stoploss']):
                        if(self.admin['live']):
                            self.close_trade(pos)
                        pos['price_out']=pos['current_price']
                        pos['status']='CLOSED'
                        self.positions[pos['symbol']]=False

                elif(pos['type']=='SHORT'):
                    pos['pnl']=round(pos['price_in']-pos['current_price'],2)
                    if(pos['current_price']<=pos['take_profit'] or pos['current_price']>=pos['stoploss']):
                        if(self.admin['live']):
                            self.close_trade(pos)
                        pos['price_out']=pos['current_price']
                        pos['status']="CLOSED"
                        self.positions[pos['symbol']]=False

                position.update_one({"_id":pos['_id']},{"$set":pos})



    def main(self):
        minute=datetime.now(tz=pytz.timezone(data['timezone'])).minute+5
        if(minute==60):
            minute=0

        for ticker in self.admin['symbols']:

            if(self.admin['breakout_lines'][ticker][0]==0 or self.admin['breakout_lines'][ticker][1]==0):
                continue

            df=self.download_ohlc(ticker)
            signal=self.signals(ticker,df)


            if(signal=="buy"):
                self.positions[ticker]=True
            elif(signal=="sell"):
                self.positions[ticker]=True

            else:
                price=df['Close'].iloc[-1]
                high=self.admin['breakout_lines'][ticker][1]
                low=self.admin['breakout_lines'][ticker][0]

                if(price>high):
                    self.admin['breakout_lines'][ticker][1]=price

                elif(price<low):
                    self.admin.breakout_lines[ticker][0]=price


        while(datetime.now(tz=pytz.timezone(data['timezone'])).minute!=minute):
            self.close_signal()


    def run(self):
        try:

            if(self.admin['status']==False):
                return

            while True:
                logger.info("ITS LOGGGING RAPIDLY")
                self.main()
                time_now=datetime.now(tz=pytz.timezone(data['timezone']))
                if(time_now.hour>=4 and time_now.minute>=0):
                    break
        except Exception:
            error.info(str(traceback.format_exc()))
            return str(traceback.format_exc())
