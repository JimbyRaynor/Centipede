from tkinter import *
import random
import os
import sys

# to import LED
two_levels_up = os.path.abspath(os.path.join('..', '..'))
sys.path.insert(0, "/home/deck/Documents")
import LEDlib

score = 0
centipedelength = 30


# The Grid is king. If Grid[x,y] == 2 then there is a centipede there (no other objects!)
  # Do not allow two objects to be at the same spot.
  # centipede could hit bullet (sideways)
# setgrid should report error if there is another object there, ie need grid[x,y]==0
# check putblock, and move?

# make centipede longer to increase difficulty. Do not make faster
# only need one centipede list: Just add more sections to list to make more
# make rocks get smaller when hit 
# fix hit bugs

# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

SpriteWidth = 32 # height and width of sprites. Every sprite has this size. This is the "block" size

class Spriteobj:
    def __init__(self, canvas,fup="",fdown="",fright="",fleft="",xblock=0,yblock=0,dx=0,dy=0,gridtype=0,size=20):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.gridtype = gridtype
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
mainwin.geometry("1216x704")
canvas1 = Canvas(mainwin,width = 1216, height = 704, bg = "black")
canvas1.place(x=0,y=0)


def creatematrix(rows,cols):
    return [[0 for i in range(cols)] for j in range(rows)]

Grid = creatematrix(100,100)   # rows, columns

def setgrid(x,y,gtype):
    Grid[y][x] = gtype # matrices refer to y (row number) first!

def getgrid(x,y):
    return Grid[y][x] # matrices refer to y (row number) first!

def getgridnext(gameobj):
    return getgrid(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy)

def getgridobj(gameobj):
    return getgrid(gameobj.xblock,gameobj.yblock)

def setgridnext(gameobj,gtype):
    setgrid(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy,gtype)

def setgridobj(gameobj,gtype):
    setgrid(gameobj.xblock,gameobj.yblock,gtype)

def putblock(x,y,stype,dx=0,dy=0,gridtype=0):
    if getgrid(x,y) == 0:  # only one object at each location
         block = Spriteobj(canvas1,fup=stype,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy,gridtype=gridtype)
         playfield.append(block)  # to stop garbage collector removing block!
         setgrid(x,y,gridtype)
         return block
    else:
        return -1 # also need to fix move() and goto() !! Look at methods for SpriteObj

def blockmove(gameobj):
    if getgridnext(gameobj) == 0:  # only one object at each location
         setgridnext(gameobj,gameobj.gridtype)
         setgridobj(gameobj,0)
         gameobj.move()
         return 0
    else:
        return -1
    
def blockgoto(gameobj,x,y):
    if getgrid(x,y) == 0:  # only one object at each location
         setgridobj(gameobj,0)
         gameobj.goto(x,y)
         setgrid(x,y,gameobj)
         return 0
    else:
         return -1 

def getblock(x,y):
    for block in playfield:
        if (block.xblock == x) and (block.yblock == y):
            return block
    return -1

def getblocknext(gameobj):
    return getblock(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy)

def createplayfield():
    for i in range(38):
        putblock(i,0,"rock.png",gridtype=1)
        putblock(i,21,"rock.png",gridtype=1)
    for i in range(21):
        putblock(0,i,"rock.png",gridtype=1)
        putblock(37,i,"rock.png",gridtype=1)
    for i in range(1,38):
        for j in range(3,20):
            if random.randint(1,100) > 95:
                putblock(i,j,"rock.png",gridtype=1)

 

def movebody():
    for cbody in centipede:
      setgridobj(cbody,0)
      if blockmove(cbody) == -1:  # -1 means cannot move (blocked path), o/w 0 it is moved
         # go down and reverse direction
         olddx =  cbody.dx
         cbody.dx, cbody.dy = 0,1
         myblock = getblocknext(cbody) # see what is below. Is it a boulder?
         if myblock != -1:  # okay to check since (if found) myblock does not have type <int> (and so is not -1)
             if myblock.gridtype == 1: # a boulder
               if myblock.yblock < 21:
                 myblock.undraw() # remove boulder that is in the way
                 setgridobj(myblock,0)
                 playfield.remove(myblock) # blockerase function
               else:
                 blockgoto(cbody,1,15) # hit bottom, so move up 6 rows
                 cbody.dx = 1  
                 cbody.dy = 0 
         blockmove(cbody) # try to move down, something else could be in the way (if so move fails)
         cbody.dx, cbody.dy = -olddx, 0 # reverse original direction

def removeblocknext(gameobj):
    myblock = getblocknext(gameobj) 
    while myblock != -1:
        myblock.undraw()
        playfield.remove(myblock)
        myblock = getblocknext(gameobj) 
    setgridnext(gameobj,0) 

def removeblock(gameobj):
      gameobj.undraw()
      setgrid(gameobj.xblock,gameobj.yblock,0)
      playfield.remove(gameobj)

def addtoscore(amount):
    global LEDscore, score
    LEDlib.Erasepoints(canvas1,LEDscore)
    LEDscore = []
    score = score + amount
    LEDlib.ShowScore(canvas1,200,30,score, LEDscore)


def centipedetimer():
    movebody()
    mainwin.after(300,centipedetimer)

def bullettimer():
    if len(bullets) == 0: return
    for bullet in bullets.copy():
      if (getgridnext(bullet) == 0) and (bullet.yblock > 1):
         bullet.move()
      else:
         if getgridnext(bullet) == 1  and (bullet.yblock > 1) : # hit block
              removeblocknext(bullet)
              addtoscore(1)
         if getgridnext(bullet) == 2: # hit centipede
              c = getblocknext(bullet)
              centipede.remove(c)
              removeblocknext(bullet) # this will remove centipede part from playfield
              putblock(bullet.xblock+bullet.dx,bullet.yblock+bullet.dy,"rock.png",gridtype=1)
              addtoscore(10)     
         bullet.undraw()
         bullets.remove(bullet)
    mainwin.after(30,bullettimer)  

def shiptimer():
    if getgridnext(ship) == 0:
       ship.move()
    ship.dx = 0
    ship.dy = 0
    mainwin.after(150,shiptimer)  

def reload():
    ship.canfire = True


playfield = []
createplayfield()

centipede = [] 
for i in range(centipedelength,0,-1): # count backwards
    centipede.append(putblock(i,1,"bodyblue.png",dx=1,dy=0,gridtype=2))

bullets = []

ship = putblock(20,20,"gun3.png",dx=0,dy=0)
ship.canfire = True

def mykey(event):
    global score, LEDscore
    key = event.keysym
    if key == "w":
        ship.dy = -1
        ship.dx = 0
    elif key == "d":
        ship.dx = 1
        ship.dy = 0
    elif key == "a":
        ship.dx = -1
        ship.dy = 0
    elif key == "s":
        ship.dy = 1
        ship.dx = 0
    elif key == "space":
        if ship.canfire:
           blockabove =  getblock(ship.xblock,ship.yblock-1)
           if blockabove == -1:
             bullet = putblock(ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1)
             bullets.append(bullet)
             mainwin.after(30,bullettimer) 
           else:
             if getgridobj(blockabove) == 1:
                removeblock(blockabove) 
                addtoscore(1)
             if getgridobj(blockabove) == 2: # hit centipede
                centipede.remove(blockabove)
                removeblock(blockabove) # this will remove centipede part from playfield
                putblock(blockabove.xblock,blockabove.yblock,"rock.png",gridtype=1)
                addtoscore(10)
           ship.canfire = False;
           mainwin.after(400,reload)
          

mainwin.bind("<KeyPress>", mykey)

LEDscore = []

centipedetimer()
shiptimer()
bullettimer()

LEDlib.ShowScore(canvas1,200,30,score, LEDscore)
mainwin.mainloop()