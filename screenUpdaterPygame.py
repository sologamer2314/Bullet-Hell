# в этом файле происходит вся отрисовка игры

import pygame as pg

def initializePygame():
    pg.font.init()
    sc = pg.display.set_mode((500,500),pg.DOUBLEBUF)
    return(sc)

def onCycle(sc,data,myselfData):
    sc.fill((0,0,0)) # Залить окно черным цветом
    try:
        for player in data["players"].keys(): # Нарисовать каждого челика
            pg.draw.rect(sc,data["players"][player]["MyColor"],(data["players"][player]["x"],data["players"][player]["y"],20,20))
    except:
        pass
    try:
        for bd in data["bullets"]: # Нарисовать каждую пулю
            pg.draw.rect(sc,(255,0,0),(bd["x"],bd["y"],10,10))
    except:
        pass
    try:
        for bd in data["bulletDangers"]: # Нарисовать каждое предупреждение пули
            pg.draw.rect(sc,bd["color"],(bd["x"],bd["y"],10,10))
    except:
        pass
    try:
        for key in data["backTextObjects"]: # Нарисовать каждый текст(позади интерфейса)

            if key["alignment"] == "upperLeft": # Если текст центрован как обычно...
                font = pg.font.SysFont("Calibri",key["size"])
                text = font.render(key["text"],key["smoothing"],key["color"],key["BGColor"])
                sc.blit(text,(key["x"],data["backTextObjects"][key]["y"]))

            if key["alignment"] == "center": # И если текст должен быть четко в середине...
                font = pg.font.SysFont("Calibri",key["size"])
                text = font.render(key["text"],key["smoothing"],key["color"],key["BGColor"])
                place = text.get_rect(center=(key["x"],key["y"]))
                sc.blit(text,place)
    except:
        pass

    if myselfData.PingWarn != 0:
        font = pg.font.SysFont("Impact",25)
        if myselfData.PingWarn < 30:
            text = font.render("Low connection!",True,(255,0,0),(128,128,128))
        else:
            text = font.render("NO CONNECTION!",True,(255,0,0),(128,128,128))
        myselfData.PingWarn -= 1
        sc.blit(text,(0,25))

    font = pg.font.SysFont("Calibri",20)
    text = font.render(str(data["TPS"])+" TPS",True,(0,255,0))
    sc.blit(text,(450,0))

    pg.display.update() # Отобразить всё, что было нарисовано