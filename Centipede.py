from tkinter import *
import random
import os
import sys

# to import LED
two_levels_up = os.path.abspath(os.path.join('..', '..'))
sys.path.insert(0, "/home/deck/Documents")
import LEDlib
from GridLib import *

score = 0
centipedelength = 30


# centipede could hit bullet (sideways)

# make centipede longer to increase difficulty. Do not make faster
# only need one centipede list: Just add more sections to list to make more
# make rocks get smaller when hit 

# for loading files (.png), set current directory = location of this python script (needed for Linux)
current_script_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_script_directory)

        
mainwin = Tk(className = "Centipede")
mainwin.geometry("1216x704")
canvas1 = Canvas(mainwin,width = 1216, height = 704, bg = "black")
canvas1.place(x=0,y=0)


def createplayfield():
    for i in range(38):
        putblock(canvas1,i,0,"rock.png",gridtype=9)
        putblock(canvas1,i,21,"rock.png",gridtype=9)
    for i in range(21):
        putblock(canvas1,0,i,"rock.png",gridtype=9)
        putblock(canvas1,37,i,"rock.png",gridtype=9)
    for i in range(1,38):
        for j in range(3,20):
            if random.randint(1,100) > 95:
                putblock(canvas1,i,j,"rock.png",gridtype=9)

 

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
                 removeblock(myblock) # remove this block because it is in the way
               else:
                 blockgoto(cbody,1,15) # hit bottom, so move up 6 rows
                 cbody.dx = 1  
                 cbody.dy = 0 
         blockmove(cbody) # try to move down, something else could be in the way (if so move fails)
         cbody.dx, cbody.dy = -olddx, 0 # reverse original direction



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
         blockmove(bullet)
      else:
         if getgridnext(bullet) in [1,2,3,4,5,6,7,8,9]  and (bullet.yblock > 1): # hit boulder
                setgridnext(bullet, getgridobj(bullet)-1)
                if getgridnext(bullet) == 0:
                   removeblock(bullet) 
                addtoscore(1)
         if getgridnext(bullet) == 2: # hit centipede
              c = getblocknext(bullet)
              centipede.remove(c)
              removeblocknext(bullet) # this will remove centipede part from playfield
              putblock(canvas1,bullet.xblock+bullet.dx,bullet.yblock+bullet.dy,"rock.png",gridtype=9)
              addtoscore(10)  
         removeblock(bullet)        
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



createplayfield()

centipede = [] 
for i in range(centipedelength,0,-1): # count backwards
    centipede.append(putblock(canvas1,i,1,"bodyblue.png",dx=1,dy=0,gridtype=20))

bullets = []

ship = putblock(canvas1,20,20,"gun3.png",dx=0,dy=0)
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
             bullet = putblock(canvas1,ship.xblock,ship.yblock-1,"bullet.png",dx=0,dy=-1,gridtype=30)
             bullets.append(bullet)
             mainwin.after(30,bullettimer) 
           else:
             if getgridobj(blockabove) in [1,2,3,4,5,6,7,8,9]: # boulder
                setgridobj(blockabove, getgridobj(blockabove)-1)
                if getgridobj(blockabove) == 0:
                   removeblock(blockabove) 
                addtoscore(1)
             if getgridobj(blockabove) == 20: # hit centipede
                centipede.remove(blockabove)
                removeblock(blockabove) # this will remove centipede part from playfield
                putblock(canvas1,blockabove.xblock,blockabove.yblock,"rock.png",gridtype=9)
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