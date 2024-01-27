import requests
import json
import jsonpath
# import websockets
# import asyncio

# tes_url = "https://api.paycorrect.fun/admin/transaction/report"
# jsondata = {
#     "Authorization":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NGE0ZjViODYyNWZkM2NlZmRmMmNiNzMiLCJ0eXBlIjoiYWRtaW4iLCJzdGF0dXMiOiJMb2dpbiIsImdlbmVyYXRlZE9uIjoxNzA2MTY1NTQxOTA3LCJpYXQiOjE3MDYxNjU1NDEsImV4cCI6MTcwNjE3Mjc0MX0.DYn5Yc-d2jwjH04vIm7CC80rKNS7YzmRPj3lQ7No3OE",
#     "Content-Type":"application/json"
# }
# metadata = {"page":1,"limit":1000,"reportTypeFilter":"deposit","entityFilter":None,"search":"TRA810989192481316080415052","receiverTypeFiler":None,"statusFilter":None,"reqTypeFilter":None}
#
# rfsd = requests.post(tes_url, headers=jsondata, json=metadata)
# print(rfsd.text)


baseurl = "https://uatapib2c.cloudd.live/api/"
file = open("E://Rock_Selenium/Apiautomation/RequestData.json", 'r')
json_input = file.read()
request_json = json.loads(json_input)
# for i in range(0,5):
login = requests.post("https://uatapib2c.cloudd.live/api/Account/AppLogin", None, request_json,headers={"sitename":"aura26"})

json_response = json.loads(login.text)
access_token = jsonpath.jsonpath(json_response,"result.access_token")
token = "bearer "+str(access_token[0])

SetRealBalanceUse = requests.post("https://uatapib2c.cloudd.live/api/Account/SetRealBalanceUse", None,headers={"Authorization":token})

ActiveMarketList = requests.post(baseurl+"Market/ActiveMarketList", None, headers={"Authorization":token})
response_data = json.loads(ActiveMarketList.text)
Betid = []
Matchid = []
for i in range(0, 300):
    toss = jsonpath.jsonpath(response_data, f"result[{i}].mn[]")
    if toss == ['TO WIN THE TOSS']:
        mid = (jsonpath.jsonpath(response_data, f"result[{i}].mid"))
        eid = (jsonpath.jsonpath(response_data, f"result[{i}].eid"))
        Betid.append(mid[0])
        Matchid.append(eid[0])
mtchid = {"matchId":Matchid[0]}
GetEventWiseMarketInfo = requests.post(baseurl+"Market/GetEventWiseMarketInfo", json=mtchid, headers={"Authorization":token})
response_data1 = json.loads(GetEventWiseMarketInfo.text)
betdetailidpath = (jsonpath.jsonpath(response_data1, "result.runnerInfo[3].rid[]"))
dict_placebet = {
    "BetId": Betid[0],
    "BetDetailId": (betdetailidpath[0]),
    "IsBack": True,
    "Rate": 1.97,
    "Stake": 100,
    "Fancytype": 10,
    "Point": 1.97,
    "placeFrom": 1,
    "deviceinfo": "browser=Chrome:: device=Desktop:: os=Windows:: latitude=0 :: longitude=0",
    "isWager": False
}
PlaceBet = requests.post(baseurl+"Bet/PlaceBet", None,dict_placebet, headers={"Authorization":token})
response_data3 = json.loads(PlaceBet.text)
print(response_data3)
assert response_data3 == "true;Bet has been placed successfully."

balance = requests.post(baseurl + "Chip/Client/Balance", None, headers={"Authorization":token})
balance_response = json.loads(balance.text)
print(balance_response)
