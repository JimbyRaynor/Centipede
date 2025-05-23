from tkinter import *
import random
import os
import sys
import time

# to import LEDlib and GridLib in Documents
# NOT NEEDED: two_levels_up = os.path.abspath(os.path.join('..', '..'))
sys.path.insert(0, "/home/deck/Documents")
import LEDlib
from GridLib import *

score = 0
centipedelength = 30

GameOver = True
GameOverSprite = 0 # created in EndGame()

# 

# PRESS the number 1 to start  (change instructions)
#   make sure CAPSLOCK is NOT down :)
#   click in this window
# draw ship destroyed  sprite
# draw centipede part
# add levels
# add text for SCORE, LEVEL , Jeff Minter style
# Draw instructions as bitmap in background (very easy, just use putblock)
# make centipede longer to increase difficulty. Do not make faster
# only need one centipede list: Just add more sections to list to make more
# add levels. 


# put flowers at bottom, if centipede hits flowers then flower gets quarter eaten and centipede goes up 6 rows
# Game ends when centipede breaks through
# use flowers to indicate level number like pacman
# Put score above rocks in black area. Look at Asterix game in GenXGrownUp

# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

        
mainwin = Tk(className = "Centipede")
mainwin.geometry("1216x800")
canvas1 = Canvas(mainwin,width = 1216, height = 800, bg = "black")
canvas1.place(x=0,y=0)



def putrock(canvas,x,y):
    putblockAni(canvas,x=x,y=y,fimages=["rock9.png","rock8.png","rock7.png","rock6.png","rock5.png","rock4.png","rock3.png","rock2.png","rock.png"],gridtype=9)

def createplayfield():
    for i in range(38):
        putrock(canvas1,x=i,y=0)
        putrock(canvas1,i,21)
    for i in range(21):
        putrock(canvas1,0,i)
        putrock(canvas1,37,i)
    for i in range(1,38):
        for j in range(3,20):
            if random.randint(1,100) > 95:
                putrock(canvas1,i,j)

 
def clearplayfield():
    tmpplayfield = playfield.copy()
    for part in tmpplayfield:
        part.undraw()
        setgridobj(part,0)

def EndGame():
    global GameOverSprite, GameOver
    setgrid(17,10,0) # need grid clear at (17,10) to place GameOverSprite, o/w putblock fails
    GameOverSprite = putblock(canvas1,17,10,"GameOver.png",dx=0,dy=0)
    GameOver = True

def movebody():
    for cbody in centipede:
      setgridobj(cbody,0)
      myblock = getblocknext(cbody)
      if myblock != -1:
          if myblock.xblock == ship.xblock and myblock.yblock == ship.yblock:
             EndGame()
      if blockmove(cbody) == -1:  # -1 means cannot move (blocked path), o/w 0 it is moved
         # go down and reverse direction
         olddx =  cbody.dx
         cbody.dx, cbody.dy = 0,1
         myblock = getblocknext(cbody) # see what is below. Is it a boulder?
         if myblock != -1:  # okay to check since (if found) myblock does not have type <int> (and so is not -1)
             if myblock.gridtype in [1,2,3,4,5,6,7,8,9]: # a boulder
               if myblock.yblock < 21:
                 removeblock(myblock) # remove this block because it is in the way
               else:
                 blockgoto(cbody,1,15) # hit bottom, so move up 6 rows
                 cbody.dx = 1  
                 cbody.dy = 0 
                 EndGame()
         blockmove(cbody) # try to move down, something else could be in the way (if so move fails)
         cbody.dx, cbody.dy = -olddx, 0 # reverse original direction



def addtoscore(amount):
    global LEDscore, score
    LEDlib.Erasepoints(canvas1,LEDscore)
    LEDscore = []
    score = score + amount
    LEDlib.ShowScore(canvas1,80,740,score, LEDscore)


def centipedetimer():
    movebody()
    if not GameOver: mainwin.after(300,centipedetimer)

def bullettimer():
    if len(bullets) == 0: return
    for bullet in bullets.copy():
      if (getgridnext(bullet) == 0) and (bullet.yblock > 1):
         blockmove(bullet)
      else:
         if getgridnext(bullet) in [1,2,3,4,5,6,7,8,9]  and (bullet.yblock > 1): # hit boulder
                rock = getblocknext(bullet)
                rock.changeimagenum(getgridnext(bullet)-2)
                if changegridnext(bullet, -1) == 0:
                   removeblocknext(bullet) 
                addtoscore(1)
         if getgridnext(bullet) == 20: # hit centipede
              c = getblocknext(bullet)
              centipede.remove(c)
              removeblocknext(bullet) # this will remove centipede part from playfield
              putrock(canvas1,bullet.xblock+bullet.dx,bullet.yblock+bullet.dy)
              addtoscore(10)  
         removeblock(bullet)        
         bullets.remove(bullet)
    if not GameOver: mainwin.after(30,bullettimer)  

def shiptimer():
    if getgridnext(ship) == 20: # centipede
         ship.move()
         EndGame() 
    elif getgridnext(ship) == 0:
         ship.move()         
    ship.dx = 0
    ship.dy = 0
    if not GameOver: mainwin.after(150,shiptimer)  

def reload():
    ship.canfire = True



createplayfield()

centipede = [] 

def createcentipede():
    for i in range(centipedelength,0,-1): # count backwards
        centipede.append(putblock(canvas1,i,1,"bodyblue.png",dx=1,dy=0,gridtype=20))

createcentipede()

bullets = []
ship = 0
def createship():
    global ship
    ship = putblock(canvas1,20,20,"gun3.png",dx=0,dy=0)
    ship.canfire = True

createship()

def mykey(event):
    global GameOver        
    key = event.keysym
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
             bullet = putblock(canvas1,ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1,gridtype=30)
             bullets.append(bullet)
             mainwin.after(30,bullettimer) 
           else:
             if getgridobj(blockabove) in [1,2,3,4,5,6,7,8,9]: # boulder
                rock = getblocknext(blockabove)
                rock.changeimagenum(getgridnext(blockabove)-2)
                if changegridnext(blockabove, -1) == 0:
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

LEDlib.ShowScore(canvas1,80,740,score, LEDscore)

def StartGame():
    global score, LEDscore, GameOver, centipede
    GameOver = False
    score = 0
    addtoscore(0) # to show updated LEDscore
    clearplayfield() 
    createplayfield()
    centipede = []
    createcentipede()
    createship()
    centipedetimer()
    shiptimer()
    bullettimer()

EndGame()

mainwin.mainloop()