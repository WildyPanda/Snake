from tkinter import *
from random import randint
from twisted.internet import task,reactor
from time import sleep

def dead():
    newGame()

def move():
    global Direction
    global GroundSize
    global Snake
    global can
    for i in range(len(Snake)):
        o = len(Snake) - 1 - i
        if(o != 0):
            if(Snake[o] != Snake[o-1]):
                if(o == len(Snake) - 1):
                    can.delete(str(Snake[o][0]) + "-" + str(Snake[o][1]))
                Snake[o] = Snake[o-1].copy()
    Snake[0][0] += Direction[0]
    Snake[0][1] += Direction[1]
    if(Snake[0][0] >= GroundSize[0]):
        Snake[0][0] -= GroundSize[0]
    if(Snake[0][0] < 0):
        Snake[0][0] = GroundSize[1] - 1
    if(Snake[0][1] >= GroundSize[1]):
        Snake[0][1] -= GroundSize[1]
    if(Snake[0][1] < 0):
        Snake[0][1] = GroundSize[1] - 1
    can.create_rectangle(Snake[0][0] * 10 + 1,Snake[0][1] * 10 + 1,(Snake[0][0] + 1) * 10 - 1,(Snake[0][1] + 1) * 10 - 1,tags = str(Snake[0][0]) + "-" + str(Snake[0][1]))
    

def eat():
    global Snake
    global ApplePos
    global can
    if(Snake[0]  == ApplePos):
        Snake.append(Snake[len(Snake) - 1])
        can.delete(str(ApplePos[0]) + "-" + str(ApplePos[1]) + "a")
        newApple()
        

def checkCollision():
    global Snake
    for i in range(1,len(Snake)):
        if(Snake[0] == Snake[i]):
            dead()
            break

def newApple():
    global Snake
    global GroundSize
    global ApplePos
    global can
    while True:
        test = True
        x = randint(0,GroundSize[0] - 1)
        y = randint(0,GroundSize[1] - 1)
        for i in Snake:
            if(i == [x,y]):
                test = False
        if(test == True):
            ApplePos = [x,y]
            can.create_oval(ApplePos[0] * 10 + 1,ApplePos[1] * 10 + 1,(ApplePos[0] + 1) * 10 - 1,(ApplePos[1] + 1) * 10 - 1,tags = str(ApplePos[0]) + "-" + str(ApplePos[1]) + "a")
            break

def updates():
    global fen
    move()
    eat()
    checkCollision()
    IAAction()
    fen.after(50,updates)

def newGame():
    global Snake
    can.delete('all')
    Direction = [1,0]
    Snake = [[0,0] , [0,1] , [0,2]]
    newApple()
    for i in Snake:
        can.create_rectangle(i[0] * 10 + 1,i[1] * 10 + 1,(i[0] + 1) * 10 - 1,(i[1] + 1) * 10 - 1,tags = str(i[0]) + "-" + str(i[1]))

def right():
    global Direction
    if(Direction != [-1,0]):
        Direction = [1,0]
        return True
    return False

def left():
    global Direction
    if(Direction != [1,0]):
        Direction = [-1,0]
        return True
    return False
    
def up():
    global Direction
    if(Direction != [0,1]):
        Direction = [0,-1]
        return True
    return False
    
def down():
    global Direction
    if(Direction != [0,-1]):
        Direction = [0,1]
        return True
    return False

def IAAction():
    global GroundSize
    global Snake
    global ApplePos
    global IaMove
    try:
        IaMove[0]
    except IndexError:
        IaMove.append("")
    if(IaMove[0] == ""):
        Pos = Snake[0].copy()
        IaMove.pop(0)
        nbTour = 0
        while True:
            nbTour += 1;
            xPosi = True
            diffX = abs(Pos[0] - ApplePos[0])
            yPosi = True
            diffY = abs(Pos[1] - ApplePos[1])
            if(Pos[0] - ApplePos[0] < 0):
                xPosi = False
            if(Pos[1] - ApplePos[1] < 0):
                yPosi = False
            if(diffX > diffY):
                if(xPosi):
                    IaMove.append("left")
                    Pos[0] += -1
                else:
                    IaMove.append("right")
                    Pos[0] += 1
            else:
                if(yPosi):
                    IaMove.append("up")
                    Pos[1] += -1
                else:
                    IaMove.append("down")
                    Pos[1] += 1
            if(Pos == ApplePos):
                break
            if(nbTour > GroundSize[0] + GroundSize[1]):
                IaMove = []
                IaMove.append("stay")
                break
        IaMove.append("")
    
    if(IaMove[0] == "up"):
        up()
    elif(IaMove[0] == "down"):
        down()
    elif(IaMove[0] == "right"):
        right()
    elif(IaMove[0] == "left"):
        left()
        
    IaMove.pop(0)
    """xPosi = True
    diffX = abs(Snake[0][0] - ApplePos[0])
    yPosi = True
    diffY = abs(Snake[0][1] - ApplePos[1])
    if(Snake[0][0] - ApplePos[0] < 0):
        xPosi = False
    if(Snake[0][0] - ApplePos[0] < 0):
        yPosi = False
    if(diffX > diffY):
        if(xPosi):
            left()
        else:
            right()
    else:
        if(yPosi):
            up()
        else:
            down()"""

fen = Tk() 
can = Canvas(fen,height = 500,width = 500)
can.pack()
can.update()

GroundSize = [can.winfo_height() // 10,can.winfo_width() // 10]
Direction = [1,0]
Snake = [[0,0] , [0,1] , [0,2]]
ApplePos = [0,0]

IaMove = [""]

newGame()
updates()

fen.mainloop()