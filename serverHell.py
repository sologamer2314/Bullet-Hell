# в этом файле будет обработка циклов игры со стороны сервера
# в сервере не нужно отображение, можно разве что добавить текст для отладки

from random import randint
import json
import socket
import pygame as pg
import serverFlipUpdater
from _thread import start_new_thread
from utilites import createData
from time import sleep, time

def launch(): # Функция запуска сервера
    global runningServer
    runningServer = True
    onLaunch()
    while runningServer: # Бесконечный цикл
        onCycle()

def waitToPlayersOnLaunch(null): #
    conn, recv = sock.accept() #
    start_new_thread(send_and_get_data, (conn,)) #
    waitToPlayersOnLaunch(None)

def specialCommandPrompt(passiveValue):
    global runningServer
    global sdcp
    while 1:
        a = input()
        if a == "exit":
            runningServer = False
        else:
            sdcp = a # special dev command prompt


def onLaunch(): # При запуске...
    global sock
    global data
    global received
    global count_of_players
    global clock
    global permissionToSend
    global data_to_send
    global tc
    global tcst
    global sdcp
    global rooms
    global receivedbuf

    receivedbuf = {}

    clock = pg.time.Clock()
    tc = 0 # tickCount
    tcst = time() # tickCountStartTime

    received = {} # Данные, полученные от игроков
    rooms = {}
    data = createData() # Создать начальные данные
    data_to_send = data # Данные для отправки

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("",4540)) # Создать сокет сервер
    count_of_players = int(input("Player count: ")) # Запросить ввод количества игроков

    sock.listen(count_of_players) # Максимальное количество прослушиваемых игроков

    permissionToSend = True # Разрешить параллельным циклам отправить данные
    start_new_thread(waitToPlayersOnLaunch, ("",))
    

    sdcp = ""

    start_new_thread(specialCommandPrompt, ("",))

    permissionToSend = False # Запретить отправку данных
    sleep(0.3) # Подождать, чтоб все параллельные циклы синхронизировались

def onCycle(): # В каждом цикле...
    global data
    global received
    global permissionToSend
    global data_to_send
    global tc
    global tcst
    global sdcp
    global rooms
    try:
        receivedbuf = received
    except:
        print("Server asynchronization!")
    receivedbuf, data, rooms = serverFlipUpdater.onFlip(receivedbuf,data,rooms,sdcp) # Провести обработку цикла сервера
    sdcp = ""

    tc += 1

    if tcst + 1.0 <= time():
        data["TPS"] = tc
        tc = 0
        tcst = time()

    data_to_send = data # Данные для отправки подготовлены
    permissionToSend = True # Разрешить отправить
    clock.tick(60) # Ограничить фпс
    permissionToSend = False # Запретить отправку

def send_and_get_data(conn): # Отправить данные клиентам и получить данные от них
    global received
    global clock
    global data_to_send
    global permissionToSend

    to_kick = False

    while 1:

        if to_kick:
            break
    
        try:
            while not permissionToSend:
                pass
            a1 = conn.recv(10000000)
            conn.send(("#####"+json.dumps(data_to_send)+"#####").encode("utf-8"))
            if a1 != None and a1 != b'':
                a2 = a1.decode("utf-8")
                try:
                    try:
                        a2 = a2.split("#####")[1]
                        a3 = json.loads(a2)
                    except:
                        to_kick = True
                        break
                    try:
                        data["players"][a3["clientID"]]
                    except:
                        try:
                            data["players"][a3["clientID"]] = {"MySize":40,"x":randint(0,500),"y":randint(0,500),"vx":0,"vy":0,"vvy":0,"MyNickname":a3["MyNickname"],"MyColor":a3["MyColor"],"vectorX":0,"vectorY":0,"upPressed":False,"downPressed":False,"leftPressed":False,"rightPressed":False}

                            print("---> Player",str(data["players"][a3["clientID"]]["MyNickname"]),"with clientID",str(a3["clientID"]),"just joined the game")
                        except:
                            to_kick = True
                            break
                    if a3["clientID"] in data["bannedIDList"]:
                        print(str(a3["clientID"])+" kicked from the server")
                        to_kick = True

                    if "quit" in a3["events"]:
                        del data["players"][a3["clientID"]]
                        break

                    # a3 ---> {"clientID":2736,"events":["quit","moveLeft","moveRight"]}
                    # data ---> {"players":{2736:{"x":23,"y":445,"vx":0,"vy":0}}}
                    try:
                        received[a3["clientID"]]["events"] = received[a3["clientID"]]["events"] + a3["events"]
                        data["players"][a3["clientID"]]["MyColor"] = a3["MyColor"]
                    except:
                        try:
                            received[a3["clientID"]] = a3
                        except Exception as e:
                            pass
                except Exception as e:
                    break
        except Exception as e:
            print(e)
            break
    # Если игрок отключился или забанен, то открыть новое подключение
    data["closed"] = True
    print("New connection is free for player.")
    conn.close()
    waitToPlayersOnLaunch(None)

launch()