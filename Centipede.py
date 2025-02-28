from tkinter import *
import random
import os

# for loading files (.png), set current directory = location of this python script
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

SpriteWidth = 20 # height and width of sprites. Every sprite has this size. This is the "block" size
class Spriteobj:
    def __init__(self, canvas,fup="",fdown="",fright="",fleft="",xblock=0,yblock=0,dx=0,dy=0,size=20):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx # 0,1,-1
        self.dy = dy # 0,1,-1
        self.canvas = canvas
        self.imageup = PhotoImage(file=fup)
        self.sprite = canvas.create_image(0,0,image=self.imageup)
        canvas.move(self.sprite, (xblock+0.5)*size,(yblock+0.5)*size)
    def move(self):
        self.xblock = self.xblock + self.dx
        self.yblock = self.yblock + self.dy
        self.canvas.move(self.sprite,self.dx*self.size,self.dy*self.size)
    def goto(self,xblock, yblock):
        self.xblock = xblock
        self.yblock = yblock 
        self.canvas.coords(self.sprite,(xblock+0.5)*self.size,(yblock+0.5)*self.size)

        
mainwin = Tk(className = "Centipede")
mainwin.geometry("800x680")
canvas1 = Canvas(mainwin,width = 800, height = 600, bg = "black")
canvas1.place(x=0,y=0)
canvastext = Canvas(mainwin,width=784,height=64, bg = "black")
canvastext.place(x=6,y=607)

font1 = ('Arial',16,"bold")
def printscr(mytext,x,y):
    canvastext.create_text(x,y,text=mytext,fill="yellow",font = font1)

printscr("Centipede",784/2,10)

def creatematrix(rows,cols):
    return [[0 for i in range(cols)] for j in range(rows)]

grid = creatematrix(100,100)   # rows, columns

def setgrid(x,y,gtype):
    grid[y][x] = gtype # matrices refer to y (row number) first!

def getgrid(x,y):
    return grid[y][x] # matrices refer to y (row number) first!

def putblock(x,y,stype,dx=0,dy=0):
    part = Spriteobj(canvas1,fup=stype,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy)
    playfield.append(part)
    grid[y][x] = 1
    return part

def createplayfield():
    for i in range(40):
        putblock(i,0,"body.png")
    for i in range(30):
        putblock(0,i,"body.png")
        putblock(39,i,"body.png")
    for i in range(2,38):
        for j in range(1,24):
            if random.randint(1,100) > 95:
                putblock(i,j,"body.png")

 

def movebody():
    for cbody in centipede:
      setgrid(cbody.xblock,cbody.yblock,0)
      if getgrid(cbody.xblock+cbody.dx,cbody.yblock+cbody.dy) == 0:
         cbody.move()
      else: # go down and reverse direction
         olddx =  cbody.dx
         cbody.dx, cbody.dy = 0,1
         cbody.move()
         cbody.dx, cbody.dy = -olddx, 0
         # remember to erase block if there is a block here
      if cbody.yblock > 29:
         cbody.goto(1,1)
         cbody.dx = 1 
      setgrid(cbody.xblock,cbody.yblock,1)

def timerupdate():
    movebody()
    mainwin.after(300,timerupdate)

playfield = []
createplayfield()

centipede = [] 
for i in range(10,0,-1): # count backwards
    centipede.append(putblock(i,1,"body.png",dx=1,dy=0))


timerupdate()
mainwin.mainloop()