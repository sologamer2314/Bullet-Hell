from math import sqrt

def createData():
    data = {} #список, который будет содержать в себе самые ценные части игры
    data["closed"] = False # закрыт ли сервер
    data["players"] = {} # данные игроков, ключ - это clientID, значение - данные
    data["backTextObjects"] = {} # тексты заднего плана {"текст объекта":{"lifeTime":60,"color":(20,100,235)}}
    data["bulletDangers"] = [] # появляющиеся пули
    data["bulletSpawnRate"] = int(((500*500)/250000)*3) # Спавнрейт пуль
    data["bullets"] = [] # Пули
    data["particles"] = [] # Частицы, продолжу делать позже
    data["TPS"] = 0
    data["bannedIDList"] = []
    return(data)

def clear_duplicates(list_): # Функция уборки дубликатов из списка,чтоб ускорить выполнение кода
    return(list(dict.fromkeys(list_)))

def TextObject(dict_,text,lifeTime,color,x,y,size,smoothing,BGColor,alignment="upperLeft"):
    dict_[text] = {"lifeTime":lifeTime,"color":color,"x":x,"y":y,"size":size,"smoothing":smoothing,"BGColor":BGColor,"alignment":alignment}
    return(dict_)

def normalizeVectors(vx,vy): # Нормализовать векторы, нужно для нахождения направления движения по вектору и улучшенного движения персонажей
    n = sqrt(pow(vx,2)+pow(vy,2))
    if n != 0:
        outx = vx/n
    else:
        outx = 0
    if n != 0:
        outy = vy/n
    else:
        outy = 0
    return(outx,outy)

def check_circles_collision(px1,py1,ps1,px2,py2,ps2):
    return(sqrt(abs(pow(px1-px2,2)+pow(py1-py2,2))) <= ps1/2+ps2/2)

def checkRectCollision(r1,r2):

    x = 0
    y = 1
    w = 2
    h = 3

    dots = [(r1[0],r1[1]),(r1[0]+r1[2],r1[1]),(r1[0],r1[1]+r1[3]),(r1[0]+r1[2],r1[1]+r1[3])]
    dots2 = [(r2[0],r2[1]),(r2[0]+r2[2],r2[1]),(r2[0],r2[1]+r2[3]),(r2[0]+r2[2],r2[1]+r2[3])]
    r = r2 # Текущий рект для проверки
    for dot in dots:
        if (r[x] <= dot[x] and r[x]+r[w] >= dot[x]) and (r[y] <= dot[y] and r[y]+r[h] >= dot[y]):
            return(True)
    
    r = r1 # Текущий рект для проверки

    for dot in dots2:
        if (r[x] <= dot[x] and r[x]+r[w] >= dot[x]) and (r[y] <= dot[y] and r[y]+r[h] >= dot[y]):
            return(True)

    return(False)

def collidelist(rect_,list_):
    fal = False
    for r in range(len(list_)):
        if checkRectCollision(rect_,list_[r]):
            fal = True
    return(fal)

def syntax(data,inp):
    if inp.find("ban ") == 0:
        data["bannedIDList"].append(inp[4:len(inp)])
        print("clientID"+str(inp[4:len(inp)])+" now in banlist!")
    if inp.find("delete player ") == 0:
        try:
            del data["players"][(inp[len("delete player "):len(inp)])]
            print("Player "+str(inp[len("delete player "):len(inp)])+" deleted succesfully!")
        except:
            print("Error at deleting a player")
    if inp.find("banlist") == 0:
        print("List of bans: "+str(data["bannedIDList"]))
    elif inp.find("unban ") == 0:
        try:
            data["bannedIDList"].remove(inp[6:len(inp)])
            print("clientID "+str(inp[6:len(inp)])+" unbanned on this server!")
        except:
            print("Error! clientID not exists in banlist!")
    elif inp.find("run ") == 0:
        try:
            eval(str(inp[4:len(inp)]))
        except:
            print("Oof!")
    return(data)