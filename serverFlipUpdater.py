# Здесь совершается обработка кадра сервера

from utilites import clear_duplicates, TextObject, normalizeVectors, check_circles_collision, collidelist, syntax
from math import sqrt
import random

def updatePlayers(received,data): # Обработка игроков

    for clientID in received:
        try:
            if received[clientID]["events"] != []:
                received[clientID]["events"] = clear_duplicates(received[clientID]["events"])

                eventName = "quit"

                if eventName in received[clientID]["events"]:
                    data["closed"] = True
                    received[clientID]["events"].remove(eventName)

                eventName = "moveUpStart"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["upPressed"] = True
                    received[clientID]["events"].remove(eventName)
                
                eventName = "moveDownStart"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["downPressed"] = True
                    received[clientID]["events"].remove(eventName)

                eventName = "moveLeftStart"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["leftPressed"] = True
                    received[clientID]["events"].remove(eventName)

                eventName = "moveRightStart"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["rightPressed"] = True
                    received[clientID]["events"].remove(eventName)

                eventName = "moveUpStop"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["upPressed"] = False
                    received[clientID]["events"].remove(eventName)

                eventName = "moveDownStop"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["downPressed"] = False
                    received[clientID]["events"].remove(eventName)

                eventName = "moveLeftStop"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["leftPressed"] = False
                    received[clientID]["events"].remove(eventName)

                eventName = "moveRightStop"

                if eventName in received[clientID]["events"]:
                    data["players"][clientID]["rightPressed"] = False
                    received[clientID]["events"].remove(eventName)

        except:
            pass

    for clientID in received:
        try:
            if received[clientID]["events"] != []:
                received[clientID]["events"] = clear_duplicates(received[clientID]["events"])

                eventName = "quit"

                if eventName in received[clientID]["events"]:
                    data["closed"] = True
                    received[clientID]["events"].remove(eventName)
        except:
            pass


    for clientID in received:
        try:
            if data["players"][clientID]["rightPressed"]:
                data["players"][clientID]["x"] += 4
            if data["players"][clientID]["leftPressed"]:
                data["players"][clientID]["x"] -= 4
            if data["players"][clientID]["upPressed"]:
                if data["players"][clientID]["y"] == 480:
                    data["players"][clientID]["vy"] -= 10
        except:
            pass

    for clientID in received:
        try:
            data["players"][clientID]["vy"] += 0.5
            data["players"][clientID]["y"] += data["players"][clientID]["vy"]
        except:
            pass


    for clientID in received:
        try:
            if data["players"][clientID]["y"] > 480:
                data["players"][clientID]["y"] = 480
                data["players"][clientID]["vy"] = 0
            if data["players"][clientID]["y"] < 0:
                data["players"][clientID]["y"] = 0
                data["players"][clientID]["vy"] = 0
            if data["players"][clientID]["x"] < 0:
                data["players"][clientID]["x"] = 0
            if data["players"][clientID]["x"] > 480:
                data["players"][clientID]["x"] = 480
        except:
            pass

    return(received,data)

def updateBackTextObjects(received,data): # Обработать текстовые объекты
    var = data
    for key in list(var["backTextObjects"]):
        if var["backTextObjects"][key]["lifeTime"] > 0:
            var["backTextObjects"][key]["lifeTime"] -= 1
        elif var["backTextObjects"][key]["lifeTime"] == -1:
            pass
        else:
            del var["backTextObjects"][key]
    for player in data["players"]:
        data["backTextObjects"] = TextObject(data["backTextObjects"],data["players"][player]["MyNickname"],1,(0,255,0),data["players"][player]["x"],data["players"][player]["y"]-30,15,True,None,alignment="center")
    return(received,var)

def updateBulletDangers(received,data):

    for x in range(data["bulletSpawnRate"]):
        chance = random.randint(1,50)
    facing_to_add_bullet = random.randint(1,3)
    if facing_to_add_bullet == 1 and chance == 1:
        data["bulletDangers"].append({"x":490,"y":random.randint(10,490),"vx":random.random()*-3,"vy":(random.random()-0.5)*3,"lt":60})
    if facing_to_add_bullet == 2 and chance == 1:
        data["bulletDangers"].append({"x":0,"y":random.randint(10,490),"vx":random.random()*3,"vy":(random.random()-0.5)*3,"lt":60})
    if facing_to_add_bullet == 3 and chance == 1:
        data["bulletDangers"].append({"x":random.randint(10,490),"y":0,"vx":(random.random()-0.5)*3,"vy":(random.random()-0.5)*3,"lt":60})

    for bd in data["bulletDangers"]:
        if bd["lt"] != 0:
            bd["color"] = (round((1 - (bd["lt"] / 60)) * 255),0,0)
        else:
            bd["color"] = (0,0,0)
        if bd["lt"] > 0:
            bd["lt"] -= 1
        elif bd["lt"] == 0:
            data["bullets"].append(bd)
            data["bulletDangers"].remove(bd)
    return(received,data)

def updateBullets(received,data):

    for bullet in data["bullets"]:
        bullet["x"] += bullet["vx"]
        bullet["y"] += bullet["vy"]

    return(received,data)
def onFlip(received,data,rooms,sdcp): # Основа...
    received, data = updatePlayers(received,data)
    received, data = updateBackTextObjects(received,data)
    received, data = updateBulletDangers(received,data)
    received, data = updateBullets(received,data)
    data = syntax(data,sdcp)
    return(received,data,rooms)