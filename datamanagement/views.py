
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


from .helpful_scripts.strategy import *
from .models import *

import threading
import random
import string
import json
import certifi
import ast

import logging
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
order=database['order']


def login_page(request):
    return render(request, "login.html")

def handleLogin(request):

    if request.user.is_authenticated:
        return redirect('/start_strategy')
    if request.method == "POST":

        loginusername = request.POST['username']
        loginpassword = request.POST['password']
        # user = authenticate(username=loginusername, password=loginpassword)
        if loginusername=="jonas_beres" and loginpassword=="tradeovate123":
            user=User.objects.get(username=loginusername)
            login(request, user)
            return redirect("../start_strategy/")
        else:
            messages.error(request, "Invalid credentials! Please try again")
            return redirect("/")
    return redirect("/")

@login_required(login_url='')
def handleLogout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='')
def rest_update(request):
    data={}
    data['admin']=admin.find_one()
    positions=list(position.find())
    if data['admin']:
        data['admin']['_id'] = str(data['admin']['_id'])
    for pos in positions:
        pos['_id'] = str(pos['_id'])
    data['present_positions']=[]
    data['closed_positions']=[]

    for pos in positions:
        if(pos['status']=="OPEN"):
            data['present_positions'].append(pos)
        else:
            data['closed_positions'].append(pos)

    return JsonResponse(data)

@login_required(login_url='')
def start_strategy(request):
    data={}
    data['admin']=admin.find_one()
    positions=list(position.find())
    data['present_positions']=[]
    data['closed_positions']=[]

    for pos in positions:
        if(pos['status']=="OPEN"):
            data['present_positions'].append(pos)
        else:
            data['closed_positions'].append(pos)

    if request.method == "POST":
        recieved_data=request.POST
        recieved_data=recieved_data.copy()

        if('status' not in recieved_data):
            recieved_data['status']='off'
        if('live' not in recieved_data):
            recieved_data['live']='off'


        MNQ_breakout_lines=recieved_data['MNQ_breakout_lines'].split(',')
        MES_breakout_lines=recieved_data['MES_breakout_lines'].split(',')
        MNQ_breakout_lines=[eval(i) for i in MNQ_breakout_lines]
        MES_breakout_lines=[eval(i) for i in MES_breakout_lines]

        breakout_lines={
            "MNQ":MNQ_breakout_lines,
            "MES":MES_breakout_lines,
        }

        params={    
            "name":recieved_data['name'],
            "password":recieved_data['password'],
            "client_id":int(recieved_data['client_id']),
            "secret_key":recieved_data['secret_key'],
            "status": True if recieved_data['status']=='on' else False,
            "live": True if recieved_data['live']=='on' else False,
            "breakout_tolerance":int(recieved_data['breakout_tolerance']),
            "wick_tolerance":int(recieved_data['wick_tolerance']),
            "risk_per_trade":int(recieved_data['risk_per_trade']),
            "max_candle_body_size":int(recieved_data['max_candle_body_size']),
            "stop_loss_historical_candles":int(recieved_data['stop_loss_historical_candles']),
            "stop_loss_wg_room":int(recieved_data['stop_loss_wg_room']),
            "time_frame":recieved_data['time_frame'],
            "breakout_lines":breakout_lines,
            # "symbols":symbols
        }
        admin.update_one({},{"$set":params})
        data['admin']=admin.find_one()
        data['admin']['breakout_lines']['MNQ']=str(data['admin']['breakout_lines']['MNQ'][0])+','+str(data['admin']['breakout_lines']['MNQ'][1])
        data['admin']['breakout_lines']['MES']=str(data['admin']['breakout_lines']['MES'][0])+','+str(data['admin']['breakout_lines']['MES'][1])
        positions=list(position.find())
        return render(request, "index.html",data)


    data['admin']['breakout_lines']['MNQ']=str(data['admin']['breakout_lines']['MNQ'][0])+','+str(data['admin']['breakout_lines']['MNQ'][1])
    data['admin']['breakout_lines']['MES']=str(data['admin']['breakout_lines']['MES'][0])+','+str(data['admin']['breakout_lines']['MES'][1])

    return render(request, "index.html",data)


def do_something():
    strat = run_strategy()
    logger.info("URL WORKED")
    value=strat.run()

def starter(request):
    t=threading.Thread(target=do_something)
    t.start()

    return JsonResponse({"SUCCESS":"URL WORKED"})