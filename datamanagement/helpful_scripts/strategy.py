import pandas as pd
import time
import traceback
from datetime import datetime
import logging

from datamanagement.models import *
from datamanagement.helpful_scripts.background_functions import *



#CONFIGURATIONS
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')




class run_strategy():

    def __init__(self, strategy):
        self.parameters = strategy
        self.ltp_prices={}
        self.times=time.time()
        self.login()

    def login():
        pass




    def add_orders(self,symbol,side,price,open_position,token_dict, dict_token):
        strategy1=orders(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time=datetime.now(),
            price=price,
            transaction_type=side,
            open_position=open_position,
            order_id=0
        )
        strategy1.save()

    def add_positions(self,symbol,side,price_in,time_out,price_out,token_dict, dict_token):


        new_position=positions(

            strategy_id=self.parameters.strategy_id,
            symbol=symbol,
            time_in=datetime.now(),
            side=str(side),
            price_in=float(price_in),
            time_out=datetime.now(),
            price_out=float(price_out),
            status="OPEN",
            token=str(token_dict[symbol])
        )
        new_position.save()


    
    def main(self,token_dict, dict_token,ws):

        pass

    def run(self):
        try:
            while True:
                self.main()
        except Exception:
            error.info(str(traceback.format_exc()))
            return str(traceback.format_exc())
