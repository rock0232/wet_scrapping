import asyncio
import datetime
import json
import requests
import websockets
import jsonpath

baseurl = "https://uatapib2c.cloudd.live/api/"
file = open("E://Rock_Selenium/Apiautomation/RequestData.json", 'r')
json_input = file.read()
request_json = json.loads(json_input)
# for i in range(0,5):
login = requests.post(f"{baseurl}Account/AppLogin", None, request_json, headers={"sitename": "aura26"})

json_response = json.loads(login.text)
access_token = jsonpath.jsonpath(json_response, "result.access_token")
token = "bearer " + str(access_token[0])

SetRealBalanceUse = requests.post(f"{baseurl}Account/SetRealBalanceUse", None, headers={"Authorization": token})

ActiveMarketList = requests.post(baseurl + "Market/ActiveMarketList", None, headers={"Authorization": token})
response_data = json.loads(ActiveMarketList.text)
Betid = []
Matchid = []
# print(response_data)
items = (response_data["result"])
for item in items:
    dates = item['ed']
    eventtype = item['st']
    marketname = item['mn']
    date = datetime.datetime.strptime(dates, "%Y-%m-%dT%H:%M:%S")
    if eventtype == 'Cricket':
        if date < datetime.datetime.now():
            if marketname == "Match Odds":
                martketid = item['mc']
                eventname = item['en']
                Betid.append(item['mid'])
                Matchid.append((item['eid']))
                # print(item['eid'])
                # print(martketid)
                # print(eventname)
    pass
print(Betid)
print(Matchid)
# if toss == ['TO WIN THE TOSS']:
#     mid = (jsonpath.jsonpath(response_data, f"result[{i}].mid"))
#     eid = (jsonpath.jsonpath(response_data, f"result[{i}].eid"))
#     Betid.append(mid[0])
#     Matchid.append(eid[0])
mtchid = {"matchId": Matchid[0]}
GetEventWiseMarketInfo = requests.post(baseurl + "Market/GetEventWiseMarketInfo", json=mtchid,
                                       headers={"Authorization": token})
response_data1 = json.loads(GetEventWiseMarketInfo.text)
# print(response_data1)
mc = (response_data1['result']['marketInfo'][0]['mc'])
print(mc)
# print((response_data1['result']['marketInfo'][0]['']))
# betdetailidpath = (jsonpath.jsonpath(response_data1, "result.runnerInfo[3].rid[]"))
betdetailidpath = (response_data1['result']['runnerInfo'][0]['rid'])
print(betdetailidpath)
print((response_data1['result']['matchInfo'][0]['en']))

websocket_server_url = 'wss://bi.cloudd.live/signalr'


async def connect_websocket(event):
    async with websockets.connect(websocket_server_url) as websocket:
        print('Connected to WebSocket server')
        await websocket.send('{"protocol":"json","version":1}')
        message = {"arguments": [f"{event}"], "invocationId": "0", "target": "ConnectMarketRate", "type": 1}
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


#
data = asyncio.get_event_loop().run_until_complete(connect_websocket(mc))
print(data)
rate = data['rate']
isback = data['isback']
print(rate, isback)

dict_placebet = {
    "BetId": Betid[0],
    "BetDetailId": betdetailidpath,
    "IsBack": isback,
    "Rate": rate,
    "Stake": 102,
    "Fancytype": 10,
    "Point": rate,
    "placeFrom": 1,
    "deviceinfo": "browser=Chrome:: device=Desktop:: os=Windows:: latitude=0 :: longitude=0",
    "isWager": False
}

balance = requests.post(baseurl + "Chip/Client/Balance", None, headers={"Authorization": token})
balance_response = json.loads(balance.text)
print(balance_response)
print(dict_placebet)

PlaceBet = requests.post(baseurl + "Bet/PlaceBet", None, dict_placebet, headers={"Authorization": token})
response_data3 = json.loads(PlaceBet.text)
print(response_data3)
try:
    assert response_data3 == "true;Bet has been placed successfully."
except:
    print("Test Failed", response_data3)

balance = requests.post(baseurl + "Chip/Client/Balance", None, headers={"Authorization": token})
balance_response = json.loads(balance.text)
print(balance_response)
print(dict_placebet)

