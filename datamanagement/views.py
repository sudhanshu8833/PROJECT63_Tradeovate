
from django.shortcuts import render
from .helpful_scripts.strategy import *
from .helpful_scripts.background_functions import *
# Create your views here.
from django.contrib import messages
import threading

import random
import string
from .models import positions, orders

import logging
logging.getLogger("pymongo").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger('dev_log')
error = logging.getLogger('error_log')





def index(request):
    logger.info("we have started logging... hurray!!")
    return render(request, "index.html")


def position(request):

    strategies = strategy.objects.filter(status="OPEN")
    lists = []
    strategy_id = []

    for i in range(len(strategies)):

        position = positions.objects.filter(
            strategy_id=strategies[i].strategy_id)
        position_list = []
        for j in range(len(position)):
            position_list.append(position[j])



        lists.append(position_list)
        strategy_id.append(strategies[i].strategy_id)

    return render(request, "position.html",    {
        'list': lists,
        'strategy_id': strategy_id
    })


def start_strategy(request):

    if request.method == "POST":

        buy_factor = request.POST['buy_factor']
        per_premium = request.POST['per_premium']
        TP1 = request.POST['TP1']
        TP2 = request.POST['TP2']
        timeout = request.POST['timeout']
        sell_factor = request.POST['sell_factor']
        lot = request.POST['lot']
        et = request.POST['et']

        try:
            type = str(request.POST['type'])

        except:
            type = 'off'

        rand_str = random_string_generator(10, string.ascii_letters)
        # obj.ltpData("NSE", 'NIFTY', "26000")['data']['ltp']
        user = User1.objects.get(username='testing')

        strategy1 = strategy(

            strategy_id=rand_str,
            buy_factor=buy_factor,
            sell_factor=sell_factor,
            percentage_premium=per_premium,
            TP1=TP1,
            TP2=TP2,
            time_out=timeout,
            LIMIT=type,
            lot=lot,
            status="OPEN",
            ET=et,
            working_days_1=user.working_days_1,
            working_days_2=user.working_days_2,
            expiry_1=user.expiry_1,
            expiry_2=user.expiry_2,
            T_now=3

        )

        strategy1.save()

        strategy1 = strategy.objects.get(strategy_id=rand_str)


        t = threading.Thread(target=do_something, args=[strategy1])
        t.setDaemon(True)
        t.start()
        

        return render(request, "index.html")

    return render(request, "index.html")

def do_something(strategy):
    strat = run_strategy(strategy)
    value=strat.run()


