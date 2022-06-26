import pygame as pg

# этот файл получает с окна ивенты(нажатие на кнопку, крестик окна и другое) и передаёт в виде списка полученных в этом кадре ивентов

def getEvents():
    
    flip_event_list = []

    for event in pg.event.get():

        if event.type is pg.QUIT: # Если игрок нажал на крестик на окне, добавить в список ивентов кадра ивент закрытия игры
            flip_event_list.append("quit")

        if event.type == pg.KEYDOWN: # Если нажата кнопка...
            if event.key == pg.K_w:
                flip_event_list.append("moveUpStart")
            if event.key == pg.K_s:
                flip_event_list.append("moveDownStart")
            if event.key == pg.K_a:
                flip_event_list.append("moveLeftStart")
            if event.key == pg.K_d:
                flip_event_list.append("moveRightStart")

        if event.type == pg.KEYUP: # Если опущена кнопка...
            if event.key == pg.K_w:
                flip_event_list.append("moveUpStop")
            if event.key == pg.K_s:
                flip_event_list.append("moveDownStop")
            if event.key == pg.K_a:
                flip_event_list.append("moveLeftStop")
            if event.key == pg.K_d:
                flip_event_list.append("moveRightStop")

    return(flip_event_list) # Вернуть список ивентов главному коду 