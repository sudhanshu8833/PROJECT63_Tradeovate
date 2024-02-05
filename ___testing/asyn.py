import asyncio
import json
import websockets
import requests
import ssl


async def connect(credentials):
    # Implement your connect logic here
    # Return the accessToken

    url = "https://live.tradovateapi.com/v1/auth/accesstokenrequest"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    data = {
        "name": "jonasberes",
        "password": "aDamko^95",
        "appId": "jonasberes",
        "appVersion": "0.0.1",
        "cid": 2493,
        "sec": "84226cf9-a8ed-41f9-999f-c44b8afa99ed",
        "deviceId":"123e4567-e89b-12d456-426619174000"
    }


    response = requests.post(url, headers=headers, json=data)

    token=response.json()['accessToken']

    return token


async def subscribe_quote(websocket, access_token):
    subscribe_message = {
  "symbol":"ESM7",
  "chartDescription": {
    "underlyingType":"MinuteBar", 
    "elementSize":15,
    "elementSizeUnit":"UnderlyingUnits", 
    "withHistogram": False
  },
  "timeRange": {
    "closestTimestamp":"2017-04-13T11:33Z",
    "closestTickId":123,
    "asFarAsTimestamp":"2017-04-13T11:33Z",
    "asMuchAsElements":66
  },
}
    await websocket.send(json.dumps(subscribe_message))

    while True:
        response = await websocket.recv()
        # Handle the response as needed
        # For example, you can parse the JSON and process the data
        if(response=='h'):
            await websocket.send('[]')

        print(response)


async def main():
    credentials = {}  # Replace with your credentials
    access_token = await connect(credentials)

    md_url = 'wss://md.tradovateapi.com/v1/websocket/md/getChart'  # Replace with your Market Data API URL

    async with websockets.connect(f"{md_url}?token={access_token}") as websocket:
        await subscribe_quote(websocket, access_token)

if __name__ == "__main__":
    asyncio.run(main())
