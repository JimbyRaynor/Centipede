
from tkinter import *
import random
import os
import sys


# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

# double size of graphics 16by16 to 32by32

# for endgame delay, explosions, ship dieing, shooting, etc just use mainwin.after(endgame,1000) 
# to start endgame 1 sec AFTER the explosion is interpreted

# to import LEDlib and GridLib in Documents
sys.path.insert(0, "/home/deck/Documents")
import LEDlib
from GridLib import *

LEVELSTART = 1
CLENGTHSTART = 6

score = 0
level = LEVELSTART
centipedelength = CLENGTHSTART

explosionlist = ["explosionBIG1.png","explosionBIG2.png","explosionBIG3.png","explosionBIG4.png","explosionBIG5.png","explosionBIG6.png","explosionBIG7.png"]
gundielist = ["guna1.png","guna2.png","guna3.png","guna4.png","guna5.png"]
tonguelist = ["tongue1.png","tongue2.png","tongue3.png","tongue4.png","tongue5.png","tongue6.png"] 
rocklist = ["rock.png","rock2.png","rock3.png","rock4.png","rock5.png","rock6.png","rock7.png","rock8.png","rock9.png"]
flowerlist = ["flower1.png","flower2.png","flower3.png","flower4.png","flower5.png"]
centipedelist = ["centipede.png","centipede2.png"] 

GameOver = True
GameOverSprite = 0 # created in EndGame()


# NOTE common tags:
# FIXME
# BUG
# HACK 
# XXX draws attention to potential buggy code
# TODO 
# Comment code for use in Python notes
# reduce/simplify code while looking for bugs
# level intermission screen
# centipedes need different colors, determined by length of centipede
#                      
# ADD to Game Over screen: 
#   click in this window to play
#   WASD arrow
#   shoot -  space bar
#   points : boulder 1
#            centipede 10*level (look at Defender/Pacman screens)
# stop centipede from eating flowers

# make fancy attract screen, maybe not. Do this last

mainwin = Tk(className = " ")
mainwin.geometry("1216x800")
canvas1 = Canvas(mainwin,width = 1216, height = 800, bg = "black")
canvas1.place(x=0,y=0)


def save_high_score(score, filename="highscore.txt"):
    with open(filename, "w") as file:  # file is automatically closed when with block is completed
        file.write(str(score))

def load_high_score(filename="highscore.txt"):
    try:
        with open(filename, "r") as file:  # file is automatically closed when with block is completed
            return int(file.read())
    except FileNotFoundError:
        return 0  # Default to 0 if no high score file exists
    
def on_close():
    save_high_score(highscore)  # Save score before exiting
    mainwin.destroy()  # Close the window
mainwin.protocol("WM_DELETE_WINDOW", on_close)  # Bind closing action

highscore = load_high_score()


def putrock(canvas,x,y):
    putblockAni(canvas,x=x,y=y,fimages=rocklist, typestring = "rock")

def putflower(canvas,x,y):
    putblockAni(canvas,x=x,y=y,fimages=flowerlist, typestring = "flower")


def createplayfield():
    random.seed(1) # same random numbers each time
    for i in range(38):
        putrock(canvas1,x=i,y=0+3)
        if i > 0 and i < 37:
            putflower(canvas1,i,21+3)
    for i in range(22):
        putrock(canvas1,0,i+3)
        putrock(canvas1,37,i+3)
    for i in range(1,38):
        for j in range(6,20):
            if random.randint(1,100) > 95:
                putrock(canvas1,i,j)

 
def clearplayfield():
    tmpplayfield = playfield.copy()
    for part in tmpplayfield:
        part.undraw()

def EndGame():
    global GameOverSprite, GameOver, level
    GameOverSprite = putblockerase(canvas1,18,10,"GameOver.png",dx=0,dy=0,typestring = "Title Screen")
    GameOver = True
    save_high_score(highscore)

def KillShip():  
    x = ship.xblock
    y = ship.yblock
    ship.undraw()
    spark = SparkAfterobj(mainwin, canvas1, fimages=gundielist,xblock=x,yblock=y,dx=0,dy=0,timealive = 1000)
    ship.xblock = 0 # to stop multiple kills by centipede!
    ship.yblock = 0
    mainwin.after(1000,EndGame) 

def killcentipedeoverlap():
    removallist = []
    for c1 in centipede:
        for c2 in centipede:
            if c1 != c2 and  c1.xblock == c2.xblock and c1.yblock == c2.yblock:
                removallist.append(c1)          
    removalset = set(removallist) # remove duplicates
    for c in removalset:
      x = c.xblock
      y = c.yblock
      c.undraw()
      centipede.remove(c)
      spark = SparkAfterobj(mainwin, canvas1, fimages=explosionlist,xblock=x,yblock=y,dx=0,dy=0,timealive = 1000)

def movebody():
    global level, centipedelength
    if len(centipede) == 0:
                 level = level + 1
                 addtoscore(0) # to show updated level
                 createcentipede()
    killcentipedeoverlap()
    for cbody in centipede:
      myblock = getblocknext(cbody)
      if cbody.yblock == 23: # eat flower
             cbody.dx, cbody.dy = 0,1
             myblock = getblocknext(cbody) 
             myblock.changeimagenum(myblock.currentimageindex+1)
             if myblock.currentimageindex >= 4:
                 spark = SparkAfterobj(mainwin, canvas1, fimages=explosionlist,xblock=myblock.xblock,yblock=myblock.yblock,dx=0,dy=0,timealive = 1000)
                 if ship.xblock != 0: # avoid mulitple kills
                     KillShip()
             blockerasegoto(cbody,1,10) # hit bottom, so move up
             cbody.dx = 1  
             cbody.dy = 0 
      if myblock != -1:
          if myblock.xblock == ship.xblock and myblock.yblock == ship.yblock:
             KillShip()  
      if blockmove(cbody) == -1:  # -1 means cannot move (blocked path), o/w 0 it is moved
         # go down and reverse direction
         olddx =  cbody.dx
         cbody.dx, cbody.dy = 0,1
         myblock = getblocknext(cbody) # see what is below. Is it a boulder?
         if myblock != -1:  # okay to check since (if found) myblock does not have type <int> (and so is not -1)
             if myblock.typestring == "rock": # a boulder
                 myblock.undraw() # remove this block because it is in the way
         blockmove(cbody) # try to move down, something else could be in the way (if so move fails)
         cbody.dx, cbody.dy = -olddx, 0 # reverse original direction


def displayscore():
    global LEDscore 
    LEDlib.Erasepoints(canvas1,LEDscore)
    LEDscore = []
    LEDlib.ShowColourText(canvas1,80+2*LEDlib.charwidth,26,"light green","SCORE", LEDscore)
    LEDlib.ShowColourScore(canvas1,80,50,"white",score, LEDscore)
    LEDlib.ShowColourText(canvas1,480,36,"light green","CENTIPEDE", LEDscore)
    LEDlib.pixellinedouble(canvas1,x=685,y=51,dx=1,dy=0,n=14,colour= "green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=727,y=51,dx=0,dy=1,n=9,colour=  "green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=727,y=75,dx=-1,dy=0,n=98,colour="green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=439,y=75,dx=0,dy=-1,n=21,colour="green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=439,y=15,dx=1,dy=0,n=98,colour= "green", LEDpoints = LEDscore)
    LEDlib.ShowColourText(canvas1,1020,26,"light green","HISCORE", LEDscore)
    LEDlib.ShowColourScore(canvas1,1020-1*LEDlib.charwidth,50,"white",highscore, LEDscore)
    LEDlib.ShowColourText(canvas1,810,26,"light blue","LEVEL", LEDscore)
    LEDlib.ShowColourScore(canvas1,810+1.5*LEDlib.charwidth,50,"light blue",level, LEDscore, numzeros = 2)

def addtoscore(amount):
    global score, highscore
    score = score + amount
    if score > highscore: highscore = score
    displayscore()

def centipedetimer():
    if not GameOver: 
        movebody()
        mainwin.after(300,centipedetimer)

def hitrock(rock):
    if rock.currentimageindex == 8 : # last bit of rock, so destroy
        rock.undraw()
    else:
        rock.changeimagenum(rock.currentimageindex+2)
    addtoscore(1)

def hitcentipede(c,nx,ny):
    centipede.remove(c)
    c.undraw() # this will remove centipede part from playfield and grid
    putrock(canvas1,nx,ny)
    spark = SparkAfterobj(mainwin, canvas1, fimages=explosionlist,xblock=nx,yblock=ny,dx=0,dy=0,timealive = 1000)
    addtoscore(10*level) 

def bullettimer():
    global level, centipedelength
    if len(bullets) == 0: return
    for bullet in bullets.copy():
      nx = bullet.xblock+bullet.dx
      ny = bullet.yblock+bullet.dy
      nextblock = getblock(nx,ny)  # block above bullet at (nx,ny)
      if nextblock  == -1:   # nothing above bullet
         blockmove(bullet)
         #bullet.move()
      else:
         if nextblock.typestring == "rock" and (bullet.yblock > 4): # hit rock
            hitrock(nextblock)             
         if nextblock.typestring == "centipede": # hit centipede
            hitcentipede(nextblock,nx,ny)
         bullet.undraw()        
         bullets.remove(bullet)
    if not GameOver: mainwin.after(30,bullettimer)  

def shiptimer():
    if ship.xblock == 0: return # ship is dead
    nextblock = getblock(ship.xblock+ship.dx, ship.yblock+ship.dy)
    if nextblock == -1: # empty space
        ship.move()
    elif nextblock.typestring == "centipede":
         ship.move()
         print("kill ship in shiptimer")
         KillShip()        
    ship.dx = 0
    ship.dy = 0
    if not GameOver: mainwin.after(150,shiptimer)  

def reload():
    ship.canfire = True

 

createplayfield()

centipede = [] 

def putcentipart(x,y,dx,dy):
    centipede.append(putblockeraseAni(mainwin, canvas = canvas1,x=x,y=y,fimages=centipedelist,dx=dx,dy=dy,delay = 300, typestring = "centipede"))


def createcentipede():
    global centipedelength
    for i in range(centipedelength,0,-1): # count backwards
        putcentipart(i,4,dx=1,dy=0)
        if level >= 3:
           putcentipart(i+25,4,dx=1,dy=0)
        if level >= 5:
           putcentipart(i,6,dx=1,dy=0)
        if level >= 6:
           putcentipart(i+25,6,dx=1,dy=0)
        if level >= 7:
           putcentipart(i,8,dx=1,dy=0)
        if level >= 8:
           putcentipart(i+25,8,dx=1,dy=0)
        if level >= 9:
           putcentipart(i,20,dx=1,dy=0)
    if level >= 9:
       centipedelength = centipedelength + 1
       if centipedelength > 11: centipedelength = 11


createcentipede()

bullets = []
ship = 0
def createship():
    global ship
    ship = putblock(canvas1,20,20,"gun3.png",dx=0,dy=0,typestring = "ship") # adds ship to playfield
    ship.canfire = True

createship()

def mykey(event):
    global GameOver        
    key = event.keysym.lower()
    if key == "1" and GameOver:
       StartGame()
    if GameOver: return
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
           spark = SparkAfterobj(mainwin, canvas1, fimages=tonguelist,xblock=ship.xblock,yblock=ship.yblock,dx=0,dy=-31,timealive = 100)
           blockabove =  getblock(ship.xblock,ship.yblock-1)
           if blockabove == -1:
             bullet = putblock(canvas1,ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1,typestring = "bullet")
             bullets.append(bullet)
             mainwin.after(30,bullettimer) 
           else:
             if blockabove.typestring == "rock" and (blockabove.yblock > 3): # hit rock
                hitrock(blockabove)
             if blockabove.typestring == "centipede": # hit centipede
                hitcentipede(blockabove,blockabove.xblock,blockabove.yblock)
           ship.canfire = False;
           mainwin.after(300,reload)
          

mainwin.bind("<KeyPress>", mykey)

LEDscore = []

displayscore()  

def StartGame():
    global score, LEDscore, GameOver, centipede, level, centipedelength
    for bullet in bullets.copy():
        bullet.undraw()
        bullets.remove(bullet)
    for c in centipede.copy():
        c.undraw()
        centipede.remove(c) 
    GameOver = False
    score = 0
    level = LEVELSTART
    addtoscore(0) # to show updated LEDscore
    clearplayfield() 
    createplayfield()
    centipede = []
    centipedelength = CLENGTHSTART
    createcentipede()
    createship()
    centipedetimer()
    shiptimer()
    bullettimer()

EndGame()

mainwin.mainloop()