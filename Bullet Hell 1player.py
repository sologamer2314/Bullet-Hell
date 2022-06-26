from typing import Text
import pygame as pg
import random
import time

from pygame import color

def launchGame():

    WIDTH = 500
    HEIGHT = 500

    pg.init()
    try:
        joystick = pg.joystick.Joystick(0)
        joystick.init()
    except:
        pass
    
    pg.display.set_caption('Bullet Hell by 5LAY3R')
    sc = pg.display.set_mode((WIDTH,HEIGHT))
    clock = pg.time.Clock()
    try:
        Font = pg.font.Font("fontPixel.ttf",20)
    except:
        Font = pg.font.Font(None,20)
    breaked_pause = False

    class World:
        def __init__(self):
            self.points = 0
            self.ticks_gone = 0
            self.bulletSpawnRate = 1

    class Player:
        def __init__(self,x,y,num,color):
            self.color = color
            self.dead = False
            self.numPlayer = num
            self.ticks_gone = 0
            self.bonus = 0
            self.points = 0
            self.x = x
            self.y = y
            self.speed = 4
            self.gravity = 0.5
            self.y_vector = 0
            self.sizeX = 20
            self.sizeY = 20
            self.jumpStrength = 10
            self.rect = pg.Rect(self.x-self.sizeX/2,self.y-self.sizeY,self.sizeX,self.sizeY)
        def getControl(self):
            if self.numPlayer == 1:
                try:
                    axis = joystick.get_axis(0)
                    axis = round(axis)
                    hat = joystick.get_hat(0)
                    jump_pressed_gamepad = joystick.get_button(0)
                except:
                    axis = 0
                    hat = []
                    hat.append(0)
                    jump_pressed_gamepad = False

                keys = pg.key.get_pressed()
                if keys[pg.K_a] or keys[pg.K_LEFT] or axis < 0 or hat[0] < 0:
                    self.x -= self.speed
                if keys[pg.K_d] or keys[pg.K_RIGHT] or axis > 0 or hat[0] > 0:
                    self.x += self.speed
                if keys[pg.K_SPACE] or keys[pg.K_UP] or jump_pressed_gamepad:
                    if self.y == HEIGHT:
                        self.y_vector = -1 * self.jumpStrength
        def update(self):
            if self.y < HEIGHT:
                self.y_vector += self.gravity
            self.y += self.y_vector
            if self.y > HEIGHT:
                self.y = HEIGHT
                self.y_vector = 0
                add_pts = 0
                for x in range(self.bonus):
                    add_pts += (x+1)
                if add_pts != 0:
                    self.bonusText = FallingText(self.x-25,self.y-40,"+"+str(add_pts),60)
                self.bonus = 0
                world.points += add_pts
            
            if self.x > WIDTH - self.sizeX/2:
                self.x = WIDTH - self.sizeX/2
            if self.x < 0 + self.sizeX/2:
                self.x = 0 + self.sizeX/2
            self.rect = pg.Rect(self.x-self.sizeX/2,self.y-self.sizeY,self.sizeX,self.sizeY)
        def show(self):
            pg.draw.rect(sc,self.color,self.rect)
        def death(self):
            self.dead = True
            for x in range(random.randint(20,40)):
                particles.append(Particle2(self.x,self.y-5,(random.random()-0.5)*5,(random.random()-0.7)*3,random.randint(10000,10000),random.random()*4,self.color))
            self.rect = pg.Rect(1000000,1000000,self.sizeX,self.sizeY)
        def revive(self):
            self.dead = False
            for obj in objects:
                for x in range(random.randint(10,25)):
                    particles.append(Particle1(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(30,100),random.random()*4))


    class DangerBullet1:
        def __init__(self,x,y,vx,vy,lt):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.lifetime = lt
            self.startlife = world.ticks_gone
        def update(self):
            self.lived = round(((world.ticks_gone - self.startlife) / self.lifetime) * 255)
        def timeKill(self):
            if world.ticks_gone - self.startlife >= self.lifetime:
                return(True)
        def draw(self):
            pg.draw.rect(sc,(self.lived,0,0),(self.x-10,self.y-10,10,10))

    class Bullet:
        def __init__(self,x,y,vx,vy):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.sizeX = 10
            self.sizeY = 10
            self.rect = pg.Rect(self.x-self.sizeX,self.y-self.sizeY,self.sizeX,self.sizeY)
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.rect = pg.Rect(self.x-self.sizeX,self.y-self.sizeY,self.sizeX,self.sizeY)
        def draw(self):
            pg.draw.rect(sc,(255,0,0),self.rect)

    class DangerReviveBox1:
        def __init__(self,x,y,vx,vy,lt):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.lifetime = lt
            self.startlife = world.ticks_gone
        def update(self):
            self.lived = round(((world.ticks_gone - self.startlife) / self.lifetime) * 255)
        def timeKill(self):
            if world.ticks_gone - self.startlife >= self.lifetime:
                return(True)
        def draw(self):
            pg.draw.rect(sc,(self.lived,self.lived,self.lived),(self.x-10,self.y-10,10,10))

    class ReviveBox:
        def __init__(self,x,y,vx,vy):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.sizeX = 10
            self.sizeY = 10
            self.rect = pg.Rect(self.x-self.sizeX,self.y-self.sizeY,self.sizeX,self.sizeY)
        def update(self):
            self.x += self.vx
            self.y += self.vy
            self.rect = pg.Rect(self.x-self.sizeX,self.y-self.sizeY,self.sizeX,self.sizeY)
        def draw(self):
            pg.draw.rect(sc,(255,255,255),self.rect)

    class Particle1:
        def __init__(self,x,y,vx,vy,lt,size,color=(255,0,0)):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.lifetime = lt
            self.startlife = world.ticks_gone
            self.size = size
            self.vvy = 0
            self.color = color
        def update(self):
            self.x += self.vx
            self.y += self.vy
            if self.y < HEIGHT-self.size:
                self.vvy += 0.25
            else:
                self.vvy = 0
                self.y = HEIGHT+1-self.size
                self.vx = 0
                self.vy = 0
            self.y += self.vvy
        def draw(self):
            pg.draw.circle(sc,self.color,(self.x,self.y),self.size)
        def timeKill(self):
            if world.ticks_gone - self.startlife >= self.lifetime:
                return(True)

    class Particle2:
        def __init__(self,x,y,vx,vy,lt,size,color=(255,0,0)):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.lifetime = lt
            self.startlife = world.ticks_gone
            self.size = size
            self.vvy = 0
            self.color = color
        def update(self):
            self.x += self.vx
            self.y += self.vy
            if self.y < HEIGHT-self.size:
                self.vvy += 0.25
            else:
                self.vvy = 0
                self.y = HEIGHT+1-self.size
                self.vx = 0
                self.vy = 0
            self.y += self.vvy
        def draw(self):
            pg.draw.rect(sc,self.color,(self.x-self.size,self.y-self.size,self.size*2,self.size*2))
        def timeKill(self):
            if world.ticks_gone - self.startlife >= self.lifetime:
                return(True)

    class FallingText:
        def __init__(self,x,y,text,lt):
            self.x = x
            self.y = y
            self.text = text
            self.lifetime = lt
            self.startlife = world.ticks_gone
        def show(self):
            self.lived = 255 - (round(((world.ticks_gone - self.startlife) / self.lifetime) * 255))
            sc.blit(Font.render(self.text,True,(0,self.lived,0)),(self.x,self.y))
        def timeKill(self):
            if world.ticks_gone - self.startlife >= self.lifetime:
                return(True)
    
    player1 = Player(WIDTH/2-20,HEIGHT/2,1,(0,255,0))
    world = World()
    objects = []
    particles = []
    DangerBullets1 = []
    DangerReviveBoxes1 = []
    ReviveBoxes = []

    while 1:
        sc.fill((0,0,0))

        try:
            if player1.bonusText.timeKill():
                player1.bonusText = None
            else:
                player1.bonusText.show()
        except:
            pass

        if not player1.dead:
            player1.getControl()
            player1.update()
            player1.show()
        for obj in DangerBullets1:
            if obj.timeKill():
                objects.append(Bullet(obj.x,obj.y,obj.vx,obj.vy))
                DangerBullets1.remove(obj)
            else:
                obj.update()
                obj.draw()

        for obj in DangerReviveBoxes1:
            if obj.timeKill():
                ReviveBoxes.append(ReviveBox(obj.x,obj.y,obj.vx,obj.vy))
                DangerReviveBoxes1.remove(obj)
            else:
                obj.update()
                obj.draw()

        for obj in objects:
            continue_bullet_check = True
            obj.update()
            obj.draw()
            if obj.rect.colliderect(player1.rect):
                if player1.y_vector > 0:
                    player1.y_vector = -8
                    for x in range(random.randint(10,25)):
                        particles.append(Particle1(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(30,100),random.random()*4))
                    objects.remove(obj)
                    continue_bullet_check = False
                    player1.bonus += 1
                else:
                    player1.death()
            if continue_bullet_check:
                if obj.x < 0 or obj.x > HEIGHT or obj.y < 0 or obj.y > WIDTH:
                    objects.remove(obj)


        for obj in ReviveBoxes:
            continue_bullet_check = True
            obj.update()
            obj.draw()
            if obj.rect.colliderect(player1.rect):
                if player1.y_vector > 0:
                    player1.revive()
                    objects = []
                    player1.y_vector = -8
                    player1.bonus += 2
                    for x in range(random.randint(10,25)):
                        particles.append(Particle2(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(60,150),random.random()*2,(255,255,255)))
                    ReviveBoxes.remove(obj)
                    continue_bullet_check = False
            if continue_bullet_check:
                if obj.x < 0 or obj.x > HEIGHT or obj.y < 0 or obj.y > WIDTH:
                    ReviveBoxes.remove(obj)

        for obj in particles:
            if obj.timeKill():
                particles.remove(obj)
            else:
                obj.update()
                obj.draw()

        for event in pg.event.get():
            if event.type == pg.WINDOWCLOSE:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_r:
                    return
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == pg.CONTROLLER_BUTTON_X:
                    return
            if event.type == pg.WINDOWCLOSE:
                exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.WINDOWCLOSE:
                                exit()
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_ESCAPE:
                                    breaked_pause = True
                                    break
                            if event.type == pg.JOYBUTTONDOWN:
                                if event.button == 7:
                                    breaked_pause = True
                                    break
                        for obj in objects:
                            obj.draw()
                        for obj in particles:
                            obj.draw()
                        sc.blit(Font.render(str(world.points)+" points",True,(255,128,0)),(25,25))
                        if player1.bonus != 0:
                            sc.blit(Font.render(str(player1.bonus),True,(0,255,0)),(25,50))
                        player1.show()
                        pg.draw.rect(sc,(255,255,255),(150,220,200,60))
                        pauseFont = pg.font.Font("fontPixel.ttf",50)
                        sc.blit(pauseFont.render(("PAUSED"),True,(0,0,0)),(175,230))
                        pg.display.update()
                        if breaked_pause:
                            breaked_pause = False
                            break
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == 7:
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.WINDOWCLOSE:
                                exit()
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_ESCAPE:
                                    breaked_pause = True
                                    break
                            if event.type == pg.JOYBUTTONDOWN:
                                if event.button == 7:
                                    breaked_pause = True
                                    break
                        for obj in objects:
                            obj.draw()
                        for obj in particles:
                            obj.draw()
                        sc.blit(Font.render(str(world.points)+" points",True,(255,128,0)),(25,25))
                        if player1.bonus != 0:
                            sc.blit(Font.render(str(player1.bonus),True,(0,255,0)),(25,50))
                        player1.show()
                        pg.draw.rect(sc,(255,255,255),(150,220,200,60))
                        pauseFont = pg.font.Font("fontPixel.ttf",50)
                        sc.blit(pauseFont.render(("PAUSED"),True,(0,0,0)),(175,230))
                        pg.display.update()
                        if breaked_pause:
                            breaked_pause = False
                            break
        
        

    
        for x in range(world.bulletSpawnRate):
            chance = random.randint(1,10)
            facing_to_add_bullet = random.randint(1,3)
            if facing_to_add_bullet == 1 and chance == 1:
                DangerBullets1.append(DangerBullet1(WIDTH,random.randint(0,HEIGHT),random.random()*-3,(random.random()-0.5)*3,60))
            if facing_to_add_bullet == 2 and chance == 1:
                DangerBullets1.append(DangerBullet1(0+10,random.randint(0,HEIGHT),random.random()*3,(random.random()-0.5)*3,60))
            if facing_to_add_bullet == 3 and chance == 1:
                DangerBullets1.append(DangerBullet1(random.randint(0,WIDTH),0+10,(random.random()-0.5)*3,(random.random()-0.5)*3,60))
        
        if player1.dead:
            sc.blit(Font.render("Game Over",True,(200,100,0)),((WIDTH/2)-50,(HEIGHT/2)-5))
        
        AddReviveIf = random.randint(1,3600)

        facing_to_add_revive = random.randint(1,3)
        if facing_to_add_revive == 1 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(WIDTH,random.randint(0,HEIGHT),random.random()*-3,(random.random()-0.5)*3,60))
        if facing_to_add_revive == 2 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(0+10,random.randint(0,HEIGHT),random.random()*3,(random.random()-0.5)*3,60))
        if facing_to_add_revive == 3 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(random.randint(0,WIDTH),0+10,(random.random()-0.5)*3,(random.random()-0.5)*3,60))

        if not player1.dead:
            sc.blit(Font.render(str(round(world.points)),True,(255,0,0)),(25,25))
        else:
            sc.blit(Font.render(str(world.points)+" points",True,(255,128,0)),(25,25))
        if player1.bonus != 0:
            sc.blit(Font.render(str(player1.bonus),True,(0,255,0)),(25,50))
        pg.display.update()
        world.ticks_gone += 1
        clock.tick(60)

while 1:
    launchGame()