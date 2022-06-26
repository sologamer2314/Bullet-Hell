import pygame as pg
import random
import time
import utilites

from pygame import color

def launchGame(keyboardActive,WIDTH,HEIGHT,fs):

    pg.init()


    class World:
        def __init__(self,WIDTH,HEIGHT):
            self.points = 0
            self.ticks_gone = 0
            # self.bulletSpawnRate = 5
            self.bulletSpawnRate = int(((WIDTH*HEIGHT)/250000)*3)

    class Player:
        def __init__(self,x,y,color,gamepad):
            self.falling = True
            self.gamepad = gamepad
            self.color = color
            self.dead = False
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
            if self.gamepad != False:
                axis = self.gamepad.get_axis(0)
                axis = round(axis)
                hat = self.gamepad.get_hat(0)
                if axis < 0 or hat[0] < 0:
                    self.x -= self.speed
                if axis > 0 or hat[0] > 0:
                    self.x += self.speed
                if self.gamepad.get_button(0):
                    if self.y == HEIGHT:
                        self.y_vector = -1 * self.jumpStrength
            else:
                keys = pg.key.get_pressed()
                if keys[pg.K_a] or keys[pg.K_LEFT]:
                    self.x -= self.speed
                if keys[pg.K_d] or keys[pg.K_RIGHT]:
                    self.x += self.speed
                if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
                    if self.y == HEIGHT:
                        self.y_vector = -1 * self.jumpStrength
        def update(self):
            if self.y < HEIGHT:
                self.y_vector += self.gravity
            self.y += self.y_vector
            if self.y >= HEIGHT:
                self.y = HEIGHT
                self.y_vector = 0
                add_pts = 0
                for x in range(self.bonus):
                    add_pts += x+1
                if add_pts != 0:
                    self.bonusText = FallingText(self.x-25,self.y-40,"+"+str(add_pts),60)
                self.bonus = 0
                world.points += add_pts
            
            if self.x > WIDTH - self.sizeX/2:
                self.x = WIDTH - self.sizeX/2
            if self.x < 0 + self.sizeX/2:
                self.x = 0 + self.sizeX/2
            self.rect = pg.Rect(self.x-self.sizeX/2,self.y-self.sizeY,self.sizeX,self.sizeY)
            self.cubeMask = pg.Surface((20,20))
            self.cubeMask.blit(sc,(self.x,self.y))
        def updateFallInfo(self):
            if self.y_vector > 0:
                self.falling = True
            else:
                self.falling = False
        def show(self):
            pg.draw.rect(sc,self.color,self.rect)
        def death(self):
            self.dead = True
            for x in range(random.randint(100,150)):
                n1, n2 = utilites.normalizeVectors((random.random()-0.5)*7,(random.random()-0.7)*3)
                n1 *= random.random()*5
                n2 *= random.random()*5
                particles.append(Particle2(self.x,self.y-5,n1,n2,random.randint(3500,3700),random.random()*4,self.color))
            self.rect = pg.Rect(1000000,1000000,self.sizeX,self.sizeY)

        def revive(self):
            self.dead = False
            for obj in world.objects:
                for x in range(random.randint(10,25)):
                    particles.append(Particle1(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(30,100),random.random()*4))
            for obj in world.ReviveBoxes:
                for x in range(random.randint(10,25)):
                    particles.append(Particle2(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(30,100),random.random()*4,(255,255,255)))
        def drawShield(self):
            pass
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

    pg.display.set_caption('Bullet Hell by 5LAY3R')

    if fs: #full screen
        sc = pg.display.set_mode((0,0),pg.FULLSCREEN)
        surface = pg.display.get_surface()
        WIDTH, HEIGHT = surface.get_width(), surface.get_height()
    else:
        sc = pg.display.set_mode((WIDTH,HEIGHT))

    players = []
    world = World(WIDTH,HEIGHT)
    world.objects = []
    particles = []
    DangerBullets1 = []
    DangerReviveBoxes1 = []
    world.ReviveBoxes = []

    count_of_gamepads = pg.joystick.get_count()
    for n in range(count_of_gamepads):
        players.append(Player(WIDTH/2,HEIGHT/2,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),pg.joystick.Joystick(n)))
    if keyboardActive:
        players.append(Player(WIDTH/2,HEIGHT/2,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),False))

        COLORS = [(255,255,255),
                (128,128,128),
                (40,200,100),
                (80,100,255),
                (128,128,0),
                (64,30,255),
                (0,255,0),
                (0,128,0),
                (128,255,255)]
        random.shuffle(COLORS)

    for player_num in range(len(players)):
        count_of_players = len(players)
        player = players[player_num]
        try:
            player.color = COLORS[player_num]
        except:
            player.color = (random.randint(50,255),random.randint(0,255),random.randint(0,255))

    clock = pg.time.Clock()
    Font = pg.font.Font("fontPixel.ttf",20)
    world.breaked_pause = False



    def bonusTextActionOnFlip():
        for player in players:
            try:
                if player.bonusText.timeKill():
                    player.bonusText = None
                else:
                    player.bonusText.show()
            except:
                pass

    def controlPlayerIfNotDead():
        for player in players:
            if not player.dead:
                player.getControl()
                player.update()
                player.updateFallInfo()
                player.show()

    def bulletDangersOnFlip():
        for obj in DangerBullets1:
            if obj.timeKill():
                world.objects.append(Bullet(obj.x,obj.y,obj.vx,obj.vy))
                DangerBullets1.remove(obj)
            else:
                obj.update()
                obj.draw()

    def reviveBoxesDangerOnFlip():
        for obj in DangerReviveBoxes1:
            if obj.timeKill():
                world.ReviveBoxes.append(ReviveBox(obj.x,obj.y,obj.vx,obj.vy))
                DangerReviveBoxes1.remove(obj)
            else:
                obj.update()
                obj.draw()

    def updateBulletsOnFlip():
        for obj in world.objects:
            continue_bullet_check = True
            obj.update()
            obj.draw()
            for player in players:
                if obj.rect.colliderect(player.rect):
                    if player.falling:
                        player.y_vector = -7.5
                        player.y -= 8
                        for x in range(random.randint(10,25)):
                            particles.append(Particle1(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(30,100),random.random()*4))
                        world.objects.remove(obj)
                        continue_bullet_check = False
                        player.bonus += 1
                    else:
                        player.death()
            if continue_bullet_check:
                if obj.x < 0 - 20 or obj.x > WIDTH + 20 or obj.y < 0 - 20 or obj.y > HEIGHT + 20:
                    world.objects.remove(obj)

    def reviveBoxesUpdate():
        for obj in world.ReviveBoxes:
            continue_bullet_check = True
            obj.update()
            obj.draw()
            for player in players:
                if obj.rect.colliderect(player.rect):
                    if player.falling:
                        player.y_vector = -8
                        player.y -= 8
                        for player in players:
                            player.revive()
                        player.bonus += 2
                        for x in range(random.randint(10,25)):
                            particles.append(Particle2(obj.x,obj.y,(random.random()-0.5)*2,(random.random()-0.7)*2,random.randint(60,150),random.random()*2,(255,255,255)))
                        world.ReviveBoxes.remove(obj)
                        continue_bullet_check = False
                        
                        world.objects = []
                        world.ReviveBoxes = []
            if continue_bullet_check:
                if obj.x < 0 - 20 or obj.x > WIDTH + 20 or obj.y < 0 - 20 or obj.y > HEIGHT + 20:
                    try:
                        world.ReviveBoxes.remove(obj)
                    except:
                        pass

    def particlesUpdateOnFlip():
        for obj in particles:
            if obj.timeKill():
                particles.remove(obj)
            else:
                obj.update()
                obj.draw()

    def everyPlayerIsDeadCheck():
        world.EveryDead = True
        for player in players:
            if player.dead == True:
                pass
            else:
                world.EveryDead = False

    def checkButtonsOfRestart():
        for event in pg.event.get():
            if event.type == pg.WINDOWCLOSE:
                exit()
            if world.EveryDead:
                if event.type == pg.JOYBUTTONDOWN:
                    if event.button == pg.CONTROLLER_BUTTON_X:
                        return('stop')
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        return('stop')
            if event.type == pg.JOYBUTTONDOWN:
                if event.button == pg.CONTROLLER_BUTTON_B:
                    # test 
                    pass
                if event.button == 7:
                    while True:
                        for event in pg.event.get():
                            if event.type == pg.WINDOWCLOSE:
                                exit()
                            if event.type == pg.KEYDOWN:
                                if event.key == pg.K_ESCAPE:
                                    world.breaked_pause = True
                                    break
                            if event.type == pg.JOYBUTTONDOWN:
                                if event.button == 7:
                                    world.breaked_pause = True
                                    break
                        for obj in world.objects:
                            obj.draw()
                        for obj in particles:
                            obj.draw()
                        sc.blit(Font.render(str(world.points)+" points",True,(255,128,0)),(25,25))
                        for player in players:
                            if player.bonus != 0:
                                sc.blit(Font.render(str(player.bonus),True,(0,255,0)),(25,50))
                        for player in players:
                            player.show()
                        pg.draw.rect(sc,(255,255,255),(WIDTH/2-100,HEIGHT/2-30,200,60))
                        pauseFont = pg.font.Font("fontPixel.ttf",50)
                        sc.blit(pauseFont.render(("PAUSED"),True,(0,0,0)),(WIDTH/2-75,HEIGHT/2-20))
                        pg.display.update()
                        if world.breaked_pause:
                            world.breaked_pause = False
                            break

    while 1:
        sc.fill((0,0,0))

        bonusTextActionOnFlip()
        
        controlPlayerIfNotDead()

        bulletDangersOnFlip()

        reviveBoxesDangerOnFlip()

        updateBulletsOnFlip()

        reviveBoxesUpdate()
        
        particlesUpdateOnFlip()

        everyPlayerIsDeadCheck()

        if checkButtonsOfRestart() == 'stop':
            return
        
    
        for x in range(world.bulletSpawnRate):
            chance = random.randint(1,50)
            facing_to_add_bullet = random.randint(1,3)
            if facing_to_add_bullet == 1 and chance == 1:
                DangerBullets1.append(DangerBullet1(WIDTH,random.randint(0,HEIGHT),random.random()*-3,(random.random()-0.5)*3,60))
            if facing_to_add_bullet == 2 and chance == 1:
                DangerBullets1.append(DangerBullet1(0+10,random.randint(0,HEIGHT),random.random()*3,(random.random()-0.5)*3,60))
            if facing_to_add_bullet == 3 and chance == 1:
                DangerBullets1.append(DangerBullet1(random.randint(0,WIDTH),0+10,(random.random()-0.5)*3,(random.random()-0.5)*3,60))
        

        if world.EveryDead:
            sc.blit(Font.render("Game Over",True,(200,100,0)),((WIDTH/2)-50,(HEIGHT/2)-5))
            sc.blit(Font.render(str(world.points)+" points",True,(255,128,0)),(25,25))
        else:
            sc.blit(Font.render(str(round(world.points)),True,(255,0,0)),(25,25))
        
        AddReviveIf = random.randint(1,1000//world.bulletSpawnRate)

        facing_to_add_revive = random.randint(1,3)
        if facing_to_add_revive == 1 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(WIDTH,random.randint(0,HEIGHT),random.random()*-3,(random.random()-0.5)*3,60))
        if facing_to_add_revive == 2 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(0+10,random.randint(0,HEIGHT),random.random()*3,(random.random()-0.5)*3,60))
        if facing_to_add_revive == 3 and AddReviveIf == 1:
            DangerReviveBoxes1.append(DangerReviveBox1(random.randint(0,WIDTH),0+10,(random.random()-0.5)*3,(random.random()-0.5)*3,60))
        
        for player in players:
            if player.bonus != 0 and not player.dead:
                sc.blit(Font.render(str(player.bonus),True,(0,255,0)),(player.x-5,player.y-40))

        pg.display.update()
        world.ticks_gone += 1
        clock.tick(60)

keyboardActive = bool(input("Activate keyboard? True/False: "))
resolution = input("Разрешение экрана(пример - 1366x768,0 - полноэкранный режим): ")

if resolution == '0':
    WIDTH = 0
    HEIGHT = 0
    FULL_SCREEN = True
else:
    FULL_SCREEN = False
    WIDTH, HEIGHT = resolution.split("x")
    WIDTH = int(WIDTH)
    HEIGHT = int(HEIGHT)
    if WIDTH >= 500 and HEIGHT >= 500:
        pass
    else:
        print("Resolution must be more than 500 pixels on width and height!")
        print("Closing...")
        time.sleep(3)
        exit()

while 1:
    launchGame(keyboardActive,WIDTH,HEIGHT,FULL_SCREEN)