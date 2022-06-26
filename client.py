# в этом файле будет цикл игры

import json
import socket

import screenEventConverter
import screenUpdaterPygame
from random import *
import pygame as pg

class MainData:
    def __init__(self):
        self.closed = False

def launch(): # Запуск клиента из файла launcher.py
    onLaunch()

    while not data.closed: # Пока игрок не закроет игру...
        onCycle()

    sock.close() # Если произошла критическая ошибка или игрок закрыл окно - закрыть подключение к серверу 

def onLaunch(): # При запуске...

    global myselfData
    myselfData = MainData()
    myselfData.PingWarn = 0

    global data
    data = MainData() #объект, который будет содержать в себе некоторые части клиента игры, пока не задействовано

    global sock
    sock = socket.socket() #объект для подключения к хосту

    sock.connect(("127.0.0.1",4540)) # подключиться к серверу

    global MyNickname
    MyNickname = input("Nickname: ") # никнейм пользователя

    global sc
    sc = screenUpdaterPygame.initializePygame() #подключить пайгейм и создать окно

    global to_send_to_server
    to_send_to_server = {} # Данные, которые будут отправляться на сервер

    global clientID
    clientID = randint(0,99999) # АйДи клиента, по нему сервер определяет игрока

    global clock
    clock = pg.time.Clock() # Будет ограничение фпс
    
    global last_received_from_host
    last_received_from_host = {} # Данные, которые будут использоваться, если в текущем цикле полученное от сервера имеет ошибку

def onCycle(): # в каждом цикле
    global clientID
    global last_received_from_host
    global pingWarn

    to_send_to_server["MyColor"] = (0,128,255) # Цвет игрока
    to_send_to_server["MyNickname"] = MyNickname
    to_send_to_server["clientID"] = clientID
    to_send_to_server["events"] = screenEventConverter.getEvents() # Ивенты пользователя (нажатия на кнопки)
    to_send_to_server["myselfSpeed"] = 5 # Скорость игрока (ёмаёАртёмжевзломает...)
    a1 = to_send_to_server
    if a1 != None and a1 != b'': # Если данные для отпрвки на сервер не пусты, то...
        a2 = "#####"+json.dumps(a1)+"#####"
        a3 = a2.encode("utf-8")
        try: # Защита от ошибки
            sock.send(a3) # Отправить данные на сервер
            
        except: # если будет ошибка,
            pass # то пропустить эту часть кода
    else: # А если данные пусты, то отправить пакет с основными данными
        sock.send("#####{\"clientID\":"+clientID+"}#####".encode("utf-8"))
    if "quit" in to_send_to_server["events"]: # Если в нажатиях есть ивент выхода из игры, то выйти из игры
        exit()
    try:
        get = sock.recv(10000000) # Получить данные от сервера...
        decoded = get.decode("utf-8")
        decoded_truth = decoded.split("#####")[1]
        received_from_host = json.loads(decoded_truth) # Расшифровать эти данные...
        last_received_from_host = received_from_host # И на всякий случай сохранить их в буфер последних данных
    except Exception as e: # Если в блоке будет ошибка, то написать об этом и перейти к последним полученным данным
        myselfData.PingWarn += 2
        received_from_host = last_received_from_host
    screenUpdaterPygame.onCycle(sc,received_from_host,myselfData) # Обновить экран (нарисовать всё, что получено от сервера)
launch()