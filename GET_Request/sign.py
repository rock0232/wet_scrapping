import asyncio
import datetime
import json
import requests
import websockets
import jsonpath

# websocket_server_url = 'wss://bi.cloudd.live/signalr'
websocket_server_url = 'wss://uatsignalr.playsta.com/SignalR'


async def connect_websocket():
    async with websockets.connect(websocket_server_url) as websocket:
        print('Connected to WebSocket server')
        await websocket.send('{"protocol":"json","version":1}')
        # message = {"arguments": [f"{event}"], "invocationId": "0", "target": "ConnectMarketRate", "type": 1}
        message = {"arguments":[13],"invocationId":"0","target":"addClient","type":1}
        # msg = message.format(arguments="arguments",event=event)
        msg = str(message) + ''
        print(msg)
        await websocket.send(msg)
        while True:
            message = await websocket.recv()
            print(message)
            message = message[:-1]
            json_data = json.loads(message)
            try:
                rate = json_data['arguments'][0]['rt'][2]['re']
                isback = json_data['arguments'][0]['rt'][2]['ib']
                data = {'rate': rate,
                        'isback': isback}
                return data
            except:
                pass

data = asyncio.get_event_loop().run_until_complete(connect_websocket())
print(data)