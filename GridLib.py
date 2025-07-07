from tkinter import *
import threading

playfield = []

# grid not used anymore
#def creatematrix(rows,cols):
#    return [[0 for i in range(cols)] for j in range(rows)]
#Grid = creatematrix(100,100)   # rows, columns

SpriteWidth = 32 # height and width of sprites. Every sprite has this size. This is the "block" size

class Spriteobj:
    def __init__(self, canvas,fup="",fimages=[],xblock=0,yblock=0,dx=0,dy=0,size=SpriteWidth, typestring = "unknown"):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx # 0,1,-1   dx = 1 means move one block right
        self.dy = dy # 0,1,-1   dy = 1 means move one block down
        self.canfire = False;
        self.canvas = canvas
        self.images = []
        self.typestring = typestring
        self.currentimageindex = 0
        for f in fimages:
          self.images.append(PhotoImage(file=f))
        if len(fimages) > 0:
            self.sprite = canvas.create_image(0,0,image=self.images[0])
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
        if self in playfield:
            playfield.remove(self)
        else:
            print("undraw error, cannot remove, not in playfield: ", self.typestring, self.xblock, self.yblock)
            if self in centipede:
                print("in centipede list")
    def changeimagenum(self,n):
        if n < len(self.images):
           self.currentimageindex = n
           self.canvas.itemconfigure(self.sprite,image=self.images[n])
      
class SpriteobjAni:
    def __init__(self, mainwin, canvas,fimages=[],xblock=0,yblock=0,dx=0,dy=0,size=SpriteWidth, delay = 100, typestring = "unknown"):
        self.xblock = xblock # number of blocks (sprites) from left of screen # col
        self.yblock = yblock # number of blocks (sprites) down from top of screen # row
        self.size = size
        self.dx = dx # 0,1,-1   dx = 1 means move one block right
        self.dy = dy # 0,1,-1   dy = 1 means move one block down
        self.canfire = False;
        self.canvas = canvas
        self.mainwin = mainwin
        self.images = []
        self.currentimageindex = 0
        self.delay = delay
        self.typestring = typestring
        for f in fimages:
          self.images.append(PhotoImage(file=f))
        if len(fimages) > 0:
            self.sprite = canvas.create_image(0,0,image=self.images[0])
        self.canvas.move(self.sprite, (xblock+0.5)*size,(yblock+0.5)*size)
        self.changeimage()
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
        if self in playfield:
            playfield.remove(self)
        else:
            print("undraw error, cannot remove, not in playfield: ", self.typestring, self.xblock, self.yblock)
            if self in centipede:
                print("in centipede list")
    def changeimage(self):
        self.canvas.itemconfigure(self.sprite,image=self.images[self.currentimageindex])
        self.currentimageindex = self.currentimageindex + 1
        if self.currentimageindex  >= len(self.images):
            self.currentimageindex  = 0
        self.mainwin.after(self.delay,self.changeimage)



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
            

def putblock(canvas,x,y,stype="",dx=0,dy=0,typestring = "unknown"):
    if getblock(x,y) == -1:  # only one object at each location
         block = Spriteobj(canvas,fup=stype,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy,typestring = typestring)
         playfield.append(block)  # to stop garbage collector removing block!
         return block
    else:
        return -1 
    
def putblockerase(canvas,x,y,fimages=[],dx=0,dy=0,typestring = "unknown"):
    testblock = getblock(x,y)
    if testblock != -1: # block already present at (x,y)
         testblock.undraw()
    block = Spriteobj(canvas,fimages,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy,typestring = typestring)
    playfield.append(block)  # to stop garbage collector removing block!
    return block

def putblockeraseAni(mainwin,canvas,x,y,fimages=[],dx=0,dy=0, delay = 100, typestring = "unknown"):
    testblock = getblock(x,y)
    if testblock != -1: # block already present at (x,y)
         testblock.undraw()
    block = SpriteobjAni(mainwin=mainwin,canvas=canvas,fimages = fimages,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy, delay=delay, typestring = typestring)
    playfield.append(block)  # to stop garbage collector removing block!
    return block
         
    
def putblockAni(canvas,x,y,fimages=[],dx=0,dy=0, typestring = "unknown"):
    if getblock(x,y) == -1:  # only one object at each location
         block = Spriteobj(canvas,fimages=fimages,xblock=x,yblock=y,size=SpriteWidth,dx=dx,dy=dy, typestring = typestring)
         playfield.append(block)  # to stop garbage collector removing block!
         return block
    else:
         return -1 
    
def blockmove(gameobj):
    nx = gameobj.xblock+gameobj.dx
    ny = gameobj.yblock+gameobj.dy
    nextblock = getblock(nx,ny)
    if nextblock == -1:  # only one object at each location
         gameobj.move()
         return 0
    else:
         return -1
    
def blockgoto(gameobj,x,y):
    if getblock(x,y) == -1:  # only one object at each location
         gameobj.goto(x,y)
         return 0
    else:
         return -1 
    
def blockerasegoto(gameobj,x,y):    
     testblock = getblock(x,y)
     if testblock != -1: # block already present at (x,y)
         testblock.undraw()
     blockgoto(gameobj,x,y)

def getblock(x,y):
    for block in playfield:
        if (block.xblock == x) and (block.yblock == y):
            return block
    return -1

def getblocknext(gameobj):
    return getblock(gameobj.xblock+gameobj.dx,gameobj.yblock+gameobj.dy)



## not used anymore
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
