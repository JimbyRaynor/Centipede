
from tkinter import *
import random
import os
import sys
import time


# double size of graphics 16by16 to 32by32

# for endgame delay, explosions, ship dieing, shooting, etc just use mainwin.after(endgame,1000) 
# to start endgame 1 sec AFTER the explosion is interpreted

# to import LEDlib and GridLib in Documents
# NOT NEEDED: two_levels_up = os.path.abspath(os.path.join('..', '..'))
sys.path.insert(0, "/home/deck/Documents")
import LEDlib
from GridLib import *

LEVELSTART = 10
CLENGTHSTART = 10

score = 0
level = LEVELSTART
centipedelength = CLENGTHSTART

GameOver = True
GameOverSprite = 0 # created in EndGame()


# NOTE common tags:
# FIXME
# BUG
# HACK 
# XXX draws attention to potential buggy code
# TODO 
# Comment code for use in Python notes
# reduce code
# simplify code
# expolision at bottom when centipede reaches bottom of window
# test each level. From level 10 onwards a centipede starts at row 19
# add sound effects
# add bombs
#    create with XX or X    or XXX  etc
#                      X
# centipedes need different colors, determined by length of centipede, use a list to choose length, colour
#                      
# 
# BUG : playfield.remove(self) is sometimes called when self is not in playfield
# XXX : centipede disappears from screen but no new level !
# BUG : Sometimes bullets are frozen. This happens in bullettimer centipede.remove(c) is called when c is not in list
#       This error continues after gameend/restart !
#      ALSO occurs with getgridnext(bullet) : Grid[y][x] list index out of range
#      AND playfield.remove(self) self not in list--   in - - removeblock(bullet)
# ADD to Game Over screen: 
#   click in this window to play (make sure CAPSLOCK is NOT down)
#   WASD arrow
#   shoot -  space bar
#   points : boulder 1
#            centipede 10*level (look at Defender/Pacman screens)
# try to make this into a slowish strategy game
# make fancy attract screen, maybe not. Do this last
# Draw instructions as bitmap in background (very easy, just use putblock?)
# make unit for saving hiscore
# put flowers at bottom, if centipede hits flowers then flower gets quarter eaten and centipede goes to top
# Game ends when centipede breaks through
# Maybe: Queen at top spawns centipede. Has defense wall like Phoenix, but why destroy?



# put Grid codes HERE:
# blank (empty space) = 0
# boulders = 1,2,3,4,5,6,7,8,9
# ship = NOT ASSIGNED
# centipede = 20 
# Flower = 100-103

# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

        
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
    putblockAni(canvas,x=x,y=y,fimages=["rock.png","rock2.png","rock3.png","rock4.png","rock5.png","rock6.png","rock7.png","rock8.png","rock9.png"],gridtype=2, objecttype = "rock")

def putflower(canvas,x,y):
    putblockAni(canvas,x=x,y=y,fimages=["flower1.png","flower2.png","flower3.png","flower4.png","flower5.png"],gridtype=101, objecttype = "flower")


def createplayfield():
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
        setgridobj(part,0)

def EndGame():
    global GameOverSprite, GameOver, level
    GameOverSprite = putblockerase(canvas1,18,10,"GameOver.png",dx=0,dy=0,objecttype = "Title Screen")
    GameOver = True
    save_high_score(highscore)

def KillShip():
    x = ship.xblock
    y = ship.yblock
    ship.undraw()
    spark = SparkAfterobj(mainwin, canvas1, fimages=["guna1.png","guna2.png","guna3.png","guna4.png","guna5.png"],xblock=x,yblock=y,dx=0,dy=0,timealive = 1000)
    ship.xblock = 0 # to stop multiple kills by centipede!
    ship.yblock = 0
    mainwin.after(1000,EndGame) 

def movebody():
    for cbody in centipede:
      setgridobj(cbody,0)
      myblock = getblocknext(cbody)
      if cbody.yblock == 23: # eat flower
             cbody.dx, cbody.dy = 0,1
             myblock = getblocknext(cbody) 
             myblock.changeimagenum(myblock.gridtype-101+1)
             myblock.gridtype = changegrid(myblock,1)
             if myblock.gridtype > 105:
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
             if myblock.gridtype in [1,2,3,4,5,6,7,8,9]: # a boulder
                 removeblock(myblock) # remove this block because it is in the way
         blockmove(cbody) # try to move down, something else could be in the way (if so move fails)
         cbody.dx, cbody.dy = -olddx, 0 # reverse original direction


def displayscore():
    global LEDscore 
    LEDlib.Erasepoints(canvas1,LEDscore)
    LEDscore = []
    LEDlib.ShowColourText(canvas1,80+2*LEDlib.charwidth,26,"light green","SCORE", LEDscore)
    LEDlib.ShowColourScore(canvas1,80,50,"yellow",score, LEDscore)
    LEDlib.ShowColourText(canvas1,480,36,"light green","CENTIPEDE", LEDscore)
    LEDlib.pixellinedouble(canvas1,x=685,y=51,dx=1,dy=0,n=14,colour= "green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=727,y=51,dx=0,dy=1,n=9,colour=  "green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=727,y=75,dx=-1,dy=0,n=98,colour="green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=439,y=75,dx=0,dy=-1,n=21,colour="green", LEDpoints = LEDscore)
    LEDlib.pixellinetriple(canvas1,x=439,y=15,dx=1,dy=0,n=98,colour= "green", LEDpoints = LEDscore)
    LEDlib.ShowColourText(canvas1,1020,26,"light green","HISCORE", LEDscore)
    LEDlib.ShowColourScore(canvas1,1020-1*LEDlib.charwidth,50,"yellow",highscore, LEDscore)
    LEDlib.ShowColourText(canvas1,810,26,"light blue","LEVEL", LEDscore)
    LEDlib.ShowColourScore(canvas1,810+1.5*LEDlib.charwidth,50,"light blue",level, LEDscore, numzeros = 2)

def addtoscore(amount):
    global score, highscore
    score = score + amount
    if score > highscore: highscore = score
    displayscore()

def centipedetimer():
    movebody()
    if not GameOver: mainwin.after(300,centipedetimer)

def bullettimer():
    global level, centipedelength
    if len(bullets) == 0: return
    for bullet in bullets.copy():
      if (getgridnext(bullet) == 0):
         blockmove(bullet)
      else:
         if getgridnext(bullet) in [1,2,3,4,5,6,7,8,9]  and (bullet.yblock > 4): # hit boulder
                rock = getblocknext(bullet)
                rock.changeimagenum(getgridnext(bullet)+2)
                if changegridnext(bullet, +2) == 8:
                   removeblocknext(bullet) 
                addtoscore(1)
         if getgridnext(bullet) == 20: # hit centipede
              c = getblocknext(bullet)
              centipede.remove(c)
              removeblocknext(bullet) # this will remove centipede part from playfield
              putrock(canvas1,bullet.xblock+bullet.dx,bullet.yblock+bullet.dy)
              addtoscore(10*level) 
              if len(centipede) == 0:
                 level = level + 1
                 centipedelength = 6+level
                 if centipedelength > 11: centipedelength = 11
                 addtoscore(0) # to show updated level
                 createcentipede()
         removeblock(bullet)        
         bullets.remove(bullet)
    if not GameOver: mainwin.after(30,bullettimer)  

def shiptimer():
    if getgridnext(ship) == 20: # centipede
         ship.move()
         print("kill ship in shiptimer")
         KillShip()
    elif getgridnext(ship) == 0:
         ship.move()         
    ship.dx = 0
    ship.dy = 0
    if not GameOver: mainwin.after(150,shiptimer)  

def reload():
    ship.canfire = True

 

createplayfield()

centipede = [] 

def putcentipart(x,y,dx,dy):
    centipede.append(putblockeraseAni(mainwin, canvas = canvas1,x=x,y=y,fimages=["centipede.png","centipede2.png"],dx=dx,dy=dy,gridtype=20,delay = 300, objecttype = "centipede"))


def createcentipede():
    for i in range(centipedelength,0,-1): # count backwards
        putcentipart(i,20,dx=1,dy=0)
        if level >= 3:
           putcentipart(i+25,4,dx=1,dy=0)
        if level >= 6:
           putcentipart(i,5,dx=1,dy=0)
        if level >= 8:
           putcentipart(i+25,5,dx=1,dy=0)

createcentipede()

bullets = []
ship = 0
def createship():
    global ship
    ship = putblock(canvas1,20,20,"gun3.png",dx=0,dy=0,objecttype = "ship") # adds ship to playfield
    ship.canfire = True

createship()

def mykey(event):
    global GameOver        
    key = event.keysym
    if key.isupper():
        print("Warning: turn off caps lock")
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
           spark = SparkAfterobj(mainwin, canvas1, fimages=["tongue1.png","tongue2.png","tongue3.png","tongue4.png","tongue5.png","tongue6.png",],xblock=ship.xblock,yblock=ship.yblock,dx=0,dy=-31,timealive = 100)
           blockabove =  getblock(ship.xblock,ship.yblock-1)
           if blockabove == -1:
             bullet = putblock(canvas1,ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1,gridtype=30,objecttype = "bullet")
             bullets.append(bullet)
             mainwin.after(30,bullettimer) 
           else:
             if getgridobj(blockabove) in [1,2,3,4,5,6,7,8,9] and (blockabove.yblock > 4): # boulder
                rock = getblocknext(blockabove)
                rock.changeimagenum(getgridnext(blockabove)+2)
                if changegridnext(blockabove, +2) == 8:
                   removeblocknext(blockabove) 
                addtoscore(1)
             if getgridobj(blockabove) == 20: # hit centipede
                centipede.remove(blockabove)
                removeblock(blockabove) # this will remove centipede part from playfield
                putrock(canvas1,blockabove.xblock,blockabove.yblock)
                addtoscore(10)
           ship.canfire = False;
           mainwin.after(300,reload)
          

mainwin.bind("<KeyPress>", mykey)

LEDscore = []

displayscore()  

def StartGame():
    global score, LEDscore, GameOver, centipede, level, centipedelength
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