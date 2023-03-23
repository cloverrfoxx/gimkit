# by clover lmao
# gimkit.com/join bot spammer in python

import requests, websocket, threading
websocket.enableTrace(False)

def on_close(ws):
    pass

def on_open(ws):
    pass

def getGameInfo(code):
    resp=requests.post(url = 'https://www.gimkit.com/api/matchmaker/find-info-from-code', json = {'code': code})
    info = resp.json()

    if not resp.ok:
        print('1')
        print(info['message']['text'])
        return False

    return info['roomId']

def getRoomInfo(gameid, name):
    resp=requests.post(
        url = 'https://www.gimkit.com/api/matchmaker/join',
        json = {
            'roomId': gameid,
            'name': name,
            # replace clientType's value with value obtained via burp suite proxying (no automated way as of yet)
            "clientType": \
                "Gimkit Web ⁡‍⁤⁢⁡⁢‍⁤‌⁢‌‍⁡‌⁢⁡‍‍⁤⁡⁢⁣‌⁡⁡⁢‍‍‍⁡‍⁡‌⁤‍‌‍‍‌⁡⁣⁡‌⁢‌‍⁣‍⁣‍‌⁡‍⁡⁢‍⁤⁤‌⁡⁣⁣⁢‍‍⁢‌‍⁡⁤‍⁣⁡‌⁢⁡⁡⁢‍‌⁤‍‍⁡‌⁢⁡‍⁣⁡‌⁡⁡⁢‍‌‍‍⁡⁡⁢‌⁢⁣‌⁡‍⁤‍⁢‍‌‍⁢‌‍⁡‍⁡⁤⁢‍⁣⁡‌⁢⁡⁣⁡‍⁣‍⁡⁢⁡⁤‌⁡‌⁡⁢‌⁤‌‍⁢‍⁡‌⁡‌⁡⁢⁡⁢‍⁡⁢‍‍⁢‌‍⁢⁣‌‍‍⁡‍⁡‍‍⁡⁡‍‌⁢‌‍‌‍⁡‍⁢‍‍⁡⁢⁣‌‍‌⁤⁡‍⁢‍‌‍‍⁣‍⁡‌‍‌‍⁡‌‍⁢‍⁣⁢‌‍‍‍⁢⁡⁣‌‍⁡‌‍⁡⁢‍⁢⁡⁡⁢⁣‍⁤‍‍‌⁡⁢‌⁡‍⁡⁡‍⁡‌⁡‌‍‌‍⁤⁡‌⁢⁡⁡‍⁡⁡‌⁢‍‍‌⁢‌⁡⁡⁡⁡⁣‌⁡⁡⁡⁤‌⁡‍‌⁡‌‍⁣‍Client V3.1"
            }
        )
    info=resp.json()

    if not resp.ok:
        print('2')
        print(info['message']['text'])
        return False

    return (info['serverUrl'], info['roomId'], info['intentId'])

def joinGame(roomid, intentid):
    resp=requests.post(url = server+'/matchmake/joinById/'+str(roomid), json = {'intentId': intentid})
    info=resp.json()

    if not resp.ok:
        print('Unlabeled error: Could not join room')
        return False

    return (info['sessionId'], info['room']['processId'])

def startWebClient(server, procid, roomid, sessid):
    ws=websocket.WebSocketApp('wss://'+server+'/'+str(procid)+'/'+str(roomid)+'?sessionId='+str(sessid), on_close = on_close)
    ws.on_open = on_open
    ws.run_forever(reconnect=3)


print('gimkit bot spammer')

print('pls game code\n')

code=input('code: ')
name=input('name: ')
count=input('bots: ')
count=int(count)
if type(count) != type(1):
    print('Invalid bot count')
    exit()
if count > 50:
    count = 50
i = 1
print(f'Spawning {count} bots')
# clients=[]
gameid=getGameInfo(code)
if not gameid:
    exit()
while i <= count:
    print(f'Getting client info for bot {i}...')
    cname = name+str(i)

    roominfo=getRoomInfo(gameid, name) # name for same name, cname for counted name

    if not roominfo:
        exit()

    server=roominfo[0]
    roomid=roominfo[1]
    intentid=roominfo[2]

    gameinfo=joinGame(roomid, intentid)

    if not gameinfo:
        exit()

    sessid=gameinfo[0]
    procid=gameinfo[1]

    # clients.append(threading.Thread(target = startWebClient, args = (server[8:], procid, roomid, sessid)))
    threading.Thread(target = startWebClient, args = (server[8:], procid, roomid, sessid)).start()
    print('Spawned bot',cname)
    i+=1

# for client in clients:
    # client.start()
