from tkinter import *
import random
import os

# make centipede longer to increase difficulty
# split centipede in two if hit (remove the centipede block that is hit with the bullet)
# make score

# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)



SpriteWidth = 20 # height and width of sprites. Every sprite has this size. This is the "block" size
class Spriteobj:
    def __init__(self, canvas,fup="",fdown="",fright="",fleft="",xblock=0,yblock=0,dx=0,dy=0,size=20):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx # 0,1,-1   dx = 1 means move one block right
        self.dy = dy # 0,1,-1   dy = 1 means move one block down
        self.canfire = False;
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
    def undraw(self):
        self.canvas.delete(self.sprite)

        
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

def putblock(x,y,stype,dx=0,dy=0,gridtype=0):
    block = Spriteobj(canvas1,fup=stype,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy)
    playfield.append(block)  # to stop garbage collector removing block!
    setgrid(x,y,gridtype)
    return block

def getblock(x,y):
    for block in playfield:
        if (block.xblock == x) and (block.yblock == y):
            return block
    return -1

def createplayfield():
    for i in range(40):
        putblock(i,0,"body.png",gridtype=1)
    for i in range(30):
        putblock(0,i,"body.png",gridtype=1)
        putblock(39,i,"body.png",gridtype=1)
    for i in range(2,38):
        for j in range(1,24):
            if random.randint(1,100) > 95:
                putblock(i,j,"body.png",gridtype=1)

 

def movebody():
    for cbody in centipede:
      setgrid(cbody.xblock,cbody.yblock,0)
      if getgrid(cbody.xblock+cbody.dx,cbody.yblock+cbody.dy) == 0:
         cbody.move()
      else: # go down and reverse direction
         olddx =  cbody.dx
         cbody.dx, cbody.dy = 0,1
         myblock = getblock(cbody.xblock+cbody.dx, cbody.yblock+cbody.dy) 
         if myblock != -1:  # okay to check since (if found) myblock does not have type <int> (and so is not -1)
             myblock.undraw()
             playfield.remove(myblock)
         cbody.move()
         cbody.dx, cbody.dy = -olddx, 0
      if cbody.yblock > 29:
         cbody.goto(1,1)
         cbody.dx = 1 
      setgrid(cbody.xblock,cbody.yblock,1)

def timerupdate():
    movebody()
    mainwin.after(300,timerupdate)

def bullettimer():
    for bullet in bullets:
      bullet.move()
    mainwin.after(20,bullettimer)    

def reload():
    ship.canfire = True

def keytimer():
    if keys["w"]:
        ship.dy = -1
        ship.dx = 0
    elif keys["d"]:
        ship.dx = 1
        ship.dy = 0
    elif keys["a"]:
        ship.dx = -1
        ship.dy = 0
    elif keys["s"]:
        ship.dy = 1
        ship.dx = 0
    elif keys["space"]:
        if ship.canfire:
         bullet = putblock(ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1)
         bullets.append(bullet)
         ship.canfire = False;
         mainwin.after(200,reload)
    else:
        ship.dx = 0
        ship.dy = 0
    mainwin.after(10,keytimer)

def shiptimer():
    if getgrid(ship.xblock+ship.dx,ship.yblock+ship.dy) == 0:
       ship.move()
    mainwin.after(100,shiptimer)

playfield = []
createplayfield()

centipede = [] 
for i in range(8,0,-1): # count backwards
    centipede.append(putblock(i,1,"bodyblue.png",dx=1,dy=0))

bullets = []

ship = putblock(20,29,"ship.png",dx=0,dy=0)
ship.canfire = True

keys = {"w": False, "a": False, "s": False, "d": False, "space": False}

def mykey(event):
    if event.keysym in keys:
        keys[event.keysym] = True

def mykey_release(event):
    if event.keysym in keys:
        keys[event.keysym] = False

mainwin.bind("<KeyPress>", mykey)
mainwin.bind("<KeyRelease>", mykey_release)

timerupdate()
shiptimer()
bullettimer()
keytimer()
mainwin.mainloop()