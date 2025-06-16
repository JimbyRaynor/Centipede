from tkinter import *
import threading

playfield = []

def creatematrix(rows,cols):
    return [[0 for i in range(cols)] for j in range(rows)]

Grid = creatematrix(100,100)   # rows, columns

SpriteWidth = 32 # height and width of sprites. Every sprite has this size. This is the "block" size

class Spriteobj:
    def __init__(self, canvas,fup="",fimages=[],xblock=0,yblock=0,dx=0,dy=0,gridtype=0,size=SpriteWidth):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.gridtype = gridtype
        self.dx = dx # 0,1,-1   dx = 1 means move one block right
        self.dy = dy # 0,1,-1   dy = 1 means move one block down
        self.canfire = False;
        self.canvas = canvas
        self.images = []
        for f in fimages:
          self.images.append(PhotoImage(file=f))
        if len(fimages) > 0:
            self.sprite = canvas.create_image(0,0,image=self.images[len(fimages)-1])
        if fup != "":
           self.imageup = PhotoImage(file=fup)
           self.sprite = canvas.create_image(0,0,image=self.imageup)
        self.canvas.move(self.sprite, (xblock+0.5)*size,(yblock+0.5)*size)
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
        playfield.remove(self)
    def changeimagenum(self,n):
        if n < len(self.images):
           self.canvas.itemconfigure(self.sprite,image=self.images[n])
      

class Sparkobj: # not needed anymore, but interesting use of threads. Use SparkAfterobj now
    def __init__(self, canvas,fimages=[],xblock=0,yblock=0,dx=0,dy=0,size=SpriteWidth,timealive=1.0):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx 
        self.dy = dy
        self.canvas = canvas
        self.images = []
        self.currentindex = 0
        self.threadrunning = True
        self.timealive = timealive
        self.timers = []
        for f in fimages:
          self.images.append(PhotoImage(file=f))
        if len(fimages) > 0:
            self.sprite = canvas.create_image(0,0,image=self.images[len(fimages)-1])
        self.canvas.move(self.sprite, (xblock+0.5)*size+dx,(yblock+0.5)*size+dy)
        self.changeimagenum()
    def undraw(self):
        self.canvas.delete(self.sprite)
        self.threadrunning = False
        self.canceltimers()
        del self
    def canceltimers(self):
        for timer in self.timers:
            timer.cancel()
        self.timers=[]
    def changeimagenum(self):
        if self.threadrunning:
           self.canvas.itemconfigure(self.sprite,image=self.images[self.currentindex]) 
           self.currentindex = self.currentindex + 1
           if self.currentindex >= len(self.images):
              self.currentindex = 0 
              self.undraw()
           else:
              timer = threading.Timer(self.timealive/len(self.images),self.changeimagenum)
              timer.start()
              self.timers.append(timer)

class SparkAfterobj: # this is an animation object lasting timealive milliseconds. Put images in fimages list.
    def __init__(self,mainwin, canvas,fimages=[],xblock=0,yblock=0,dx=0,dy=0,size=SpriteWidth,timealive=1000):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx 
        self.dy = dy
        self.canvas = canvas
        self.mainwin = mainwin
        self.images = []
        self.currentindex = 0
        self.timealive = timealive
        for f in fimages:
          self.images.append(PhotoImage(file=f))
        if len(fimages) > 0:
            self.sprite = canvas.create_image(0,0,image=self.images[len(fimages)-1])
        self.canvas.move(self.sprite, (xblock+0.5)*size+dx,(yblock+0.5)*size+dy)
        self.changeimagenum()
    def undraw(self):
        self.canvas.delete(self.sprite)
        del self
    def changeimagenum(self):
        self.canvas.itemconfigure(self.sprite,image=self.images[self.currentindex]) 
        self.currentindex = self.currentindex + 1
        if self.currentindex >= len(self.images):
            self.currentindex = 0 
            self.undraw()
        else:
           self.mainwin.after(int(self.timealive/len(self.images)),self.changeimagenum)
            

def setgrid(x,y,gtype):
    if Grid[y][x] != 0 and gtype != 0:
        print("Error: Writing to non-zero grid (an object is already there)")
        print("Grid = ", Grid[y][x])
        print("gtype = ", gtype)
    Grid[y][x] = gtype # matrices refer to y (row number) first!

def setgridNoError(x,y,gtype):
    Grid[y][x] = gtype # matrices refer to y (row number) first!

def getgrid(x,y):
    return Grid[y][x] # matrices refer to y (row number) first!

def getgridnext(gameobj):
    return getgrid(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy)

def getgridobj(gameobj):
    return getgrid(gameobj.xblock,gameobj.yblock)

def setgridnext(gameobj,gtype):
    setgrid(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy,gtype)

def changegridnext(gameobj,dchange):
    valuegrid = getgridnext(gameobj)+dchange
    setgridNoError(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy,valuegrid)
    return valuegrid

def setgridobj(gameobj,gtype):
    setgrid(gameobj.xblock,gameobj.yblock,gtype)

def putblock(canvas,x,y,stype="",dx=0,dy=0,gridtype=0):
    if getgrid(x,y) == 0:  # only one object at each location
         block = Spriteobj(canvas,fup=stype,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy,gridtype=gridtype)
         playfield.append(block)  # to stop garbage collector removing block!
         setgrid(x,y,gridtype)
         return block
    else:
        return -1 
    
def putblockAni(canvas,x,y,fimages=[],dx=0,dy=0,gridtype=0):
    if getgrid(x,y) == 0:  # only one object at each location
         block = Spriteobj(canvas,fimages=fimages,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy,gridtype=gridtype)
         playfield.append(block)  # to stop garbage collector removing block!
         setgrid(x,y,gridtype)
         return block
    else:
        return -1 
    
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

def removeblocknext(gameobj): 
    myblock = getblocknext(gameobj) 
    if myblock != -1:
        myblock.undraw()
        #playfield.remove(myblock) done in undraw
    setgridnext(gameobj,0) 

def removeblock(gameobj):
      gameobj.undraw()
      setgrid(gameobj.xblock,gameobj.yblock,0)
      #playfield.remove(gameobj) done in undraw