import uuid
print(uuid.uuid5())

# import requests
# import yfinance as yf

# # data=yf.download("ES=F",period='1mo',interval='5m')
# # data.to_csv("data.csv")
# url = "https://live.tradovateapi.com/v1/auth/accesstokenrequest"

# headers = {
#     "Content-Type": "application/json",
#     "Accept": "application/json"
# }

data = {
    "name": "jonasberes",
    "password": "aDamko^95",
    "appId": "jonasberes",
    "appVersion": "0.0.1",
    "cid": 2493,
    "sec": "84226cf9-a8ed-41f9-999f-c44b8afa99ed",
    "deviceId":"123e4567-e89b-12d456-426619174000"
}


# response = requests.post(url, headers=headers, json=data)
# print(response)
# print(response.status_code)
# print(response.json())


# # # api = "https://md.tradovateapi.com/md/getChart"

# # # # params={
# # # #   "symbol":"ESM7",
# # # #   "chartDescription": {
# # # #     "underlyingType":"MinuteBar", 
# # # #     "elementSize":15,
# # # #     "elementSizeUnit":"UnderlyingUnits",
# # # #     "withHistogram": False
# # # #   },
# # # #   "timeRange": {
# # # #     "closestTimestamp":"2017-04-13T11:33Z",
# # # #     "closestTickId":123,
# # # #     "asFarAsTimestamp":"2017-04-13T11:33Z",
# # # #     "asMuchAsElements":66
# # # #   },
# # # # }
# # # response=requests.get(api,headers=headers,json=params)
# # # # print(response.json())
# # # print(response.text)
import certifi
print(certifi.where())
