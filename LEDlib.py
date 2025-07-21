
# TODO
# Make load/save easier

psize = 3
charwidth = 23

ONE = [(1,6), (2,1), (2,6), (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (5,6), (6,6)]
ZERO = [(0,2), (0,3), (0,4), (0,5), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,2), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,1), (6,2), (6,3), (6,4), (6,5)]
TWO = [(0,1), (1,0), (1,1), (1,2), (1,6), (2,0), (2,2), (2,5), (2,6), (3,0), (3,4), (3,5), (3,6), (4,0), (4,4), (4,6), (5,0), (5,1), (5,2), (5,3), (5,6), (6,1), (6,2), (6,3), (6,5), (6,6)]
THREE = [(0,1), (0,5), (1,0), (1,1), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,1), (6,2), (6,4), (6,5)]
FOUR = [(0,3), (0,4), (1,2), (1,3), (1,4), (2,1), (2,2), (2,4), (3,0), (3,1), (3,4), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,4)]
FIVE = [(0,0), (0,1), (0,2), (0,3), (0,5), (1,0), (1,1), (1,2), (1,3), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,3), (5,4), (5,5), (5,6), (6,0), (6,1), (6,4), (6,5)]
SIX = [(0,1), (0,2), (0,3), (0,4), (0,5), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,1), (5,3), (5,4), (5,5), (5,6), (6,1), (6,4), (6,5)]
SEVEN = [(0,0), (0,1), (1,0), (1,1), (2,0), (2,5), (2,6), (3,0), (3,3), (3,4), (3,5), (3,6), (4,0), (4,1), (4,2), (4,3), (4,4), (5,0), (5,1), (5,2), (6,0), (6,1)]
EIGHT = [(0,1), (0,4), (0,5), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,1), (6,2), (6,4), (6,5)]
NINE = [(0,1), (0,2), (0,5), (1,0), (1,1), (1,2), (1,3), (1,5), (1,6), (2,0), (2,3), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,5), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (6,1), (6,2), (6,3), (6,4)]

# leave rightmost column blank
# leave bottom row blank  
charA = []
charB = []
charC = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,6), (4,0), (4,6), (5,0), (5,1), (5,5), (5,6), (6,0), (6,1), (6,5), (6,6)]
charD = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,6), (4,0), (4,1), (4,6), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,2), (6,3), (6,4), (6,5), (6,6)]
charE = [(0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,6), (6,0), (6,1), (6,5), (6,6)]
charF = []
charG = []
charH = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,3), (4,3), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6)]
charI = [(1,0), (1,6), (2,0), (2,4), (2,5), (2,6), (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (5,0), (5,6)]
charJ = []
charK = []
charL = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,6), (4,6), (5,6), (6,5), (6,6)]
charM = []
charN = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,1), (3,2), (3,3), (4,2), (4,3), (4,4), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6)]
charO = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,6), (4,0), (4,6), (5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6)]
charP = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,3), (4,0), (4,3), (5,0), (5,1), (5,2), (5,3), (6,0), (6,1), (6,2), (6,3)]
charQ = []
charR = [(0,4), (0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (3,0), (3,3), (3,4), (4,0), (4,3), (4,4), (4,5), (5,0), (5,1), (5,2), (5,3), (5,5), (5,6), (6,1), (6,2), (6,6)]
charS = [(0,5), (0,6), (1,0), (1,1), (1,2), (1,3), (1,5), (1,6), (2,0), (2,1), (2,2), (2,3), (2,5), (2,6), (3,0), (3,3), (3,6), (4,0), (4,3), (4,6), (5,0), (5,1), (5,3), (5,4), (5,5), (5,6), (6,0), (6,1), (6,3), (6,4), (6,5), (6,6)]
charT = [(1,0), (2,0), (2,4), (2,5), (2,6), (3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (5,0), (6,0)]
charU = []
charV = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (2,0), (2,3), (2,4), (2,5), (2,6), (3,5), (3,6), (4,3), (4,4), (4,5), (5,0), (5,1), (5,2), (5,3), (5,4), (6,0), (6,1), (6,2)]
charW = []
charX = []
charY = []
charZ = []


def createLED(canvas, x,y, LEDpoints):
 p1 = canvas.create_rectangle(x, y, x+psize, y+psize, fill="black")
 p2 = canvas.create_oval(x, y, x+psize, y+psize, fill="white")
 LEDpoints.append(p1)
 LEDpoints.append(p2)

def createLEDcolour(canvas, x,y, colour, LEDpoints):
 p1 = canvas.create_rectangle(x, y, x+psize, y+psize, fill="black")
 p2 = canvas.create_oval(x, y, x+psize, y+psize, fill=colour)
 #p2 = canvas.create_rectangle(x, y, x+psize-1, y+psize-1, fill=colour)
 LEDpoints.append(p1)
 LEDpoints.append(p2)

def createLEDcolourSolid(canvas, x,y, colour, LEDpoints):
 p2 = canvas.create_rectangle(x, y, x+psize, y+psize, fill=colour, outline = "")
 LEDpoints.append(p2)

# white char
def createChar(canvas,x,y,points, LEDpoints):
  prect = canvas.create_rectangle(x, y, x+psize*8, y+psize*8, fill="black") # erase background for new char
  LEDpoints.append(prect)
  for p in points:
    createLED(canvas,x+p[0]*psize,y+p[1]*psize, LEDpoints)

# All one colour char
def createCharBlockColour(canvas,x,y,colour, points, LEDpoints):
  prect = canvas.create_rectangle(x, y, x+psize*8, y+psize*8, fill="black") # erase background for new char
  LEDpoints.append(prect)
  for p in points:
    createLEDcolour(canvas,x+p[0]*psize,y+p[1]*psize, colour, LEDpoints)    

# Multi-Colour char
def createCharColour(canvas,x,y,colourpoints, LEDpoints):
  for p in colourpoints:
    createLEDcolour(canvas,x+p[0]*psize,y+p[1]*psize,p[2], LEDpoints)

def createCharColourSolid(canvas,x,y,colourpoints, LEDpoints):
  for p in colourpoints:
    createLEDcolourSolid(canvas,x+p[0]*psize,y+p[1]*psize,p[2], LEDpoints)
  
def pixelline(canvas,x,y,dx,dy,n,colour, LEDpoints):
   for i in range(n):
       createLEDcolour(canvas, x+i*dx*psize,y+i*dy*psize,colour, LEDpoints)

def pixellinedouble(canvas,x,y,dx,dy,n,colour, LEDpoints):
   for i in range(n):
       createLEDcolour(canvas, x+i*dx*psize,y+i*dy*psize,colour, LEDpoints)
       createLEDcolour(canvas, x+i*dx*psize+dy*psize,y+i*dy*psize+dx*psize,colour, LEDpoints)

def pixellinetriple(canvas,x,y,dx,dy,n,colour, LEDpoints):
   for i in range(n):
       createLEDcolour(canvas, x+i*dx*psize,y+i*dy*psize,colour, LEDpoints)
       createLEDcolour(canvas, x+i*dx*psize+dy*psize,y+i*dy*psize+dx*psize,colour, LEDpoints)
       createLEDcolour(canvas, x+i*dx*psize+2*dy*psize,y+i*dy*psize+2*dx*psize,colour, LEDpoints)
          

# From Copilot: enumerate is a built-in Python function that makes iteration more convenient when you need both 
# an index and the value of an iterable (like a list or string).
def ShowText(canvas,x,y,mytext, LEDpoints):
    charactermap = [charA,charB,charC,charD,charE,charF,charG,charH,charI,charJ,charK,charL,charM,charN,charO,charP,charQ,charR,charS,charT,charU,charV,charW,charX,charY,charZ] 
    for i,c in enumerate(mytext):  # i=0 pairs with c = first char in mytext, i = 1 pairs with c = second char, etc
       createChar(canvas,x+i*charwidth,y,charactermap[ord(c)-65], LEDpoints)

def ShowScore(canvas,x,y,myscore, LEDpoints,numzeros=9):
    digits = [ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE]
    stringscore = str(myscore).zfill(numzeros) 
    for i,c in enumerate(stringscore):
       createChar(canvas,x+i*charwidth,y,digits[int(c)], LEDpoints)

def ShowColourScore(canvas,x,y,colour, myscore, LEDpoints,numzeros=9):
    digits = [ZERO,ONE,TWO,THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE]
    stringscore = str(myscore).zfill(numzeros) 
    for i,c in enumerate(stringscore):
       createCharBlockColour(canvas,x+i*charwidth,y,colour,digits[int(c)], LEDpoints)

def ShowColourText(canvas,x,y,colour, mytext, LEDpoints):
    charactermap = [charA,charB,charC,charD,charE,charF,charG,charH,charI,charJ,charK,charL,charM,charN,charO,charP,charQ,charR,charS,charT,charU,charV,charW,charX,charY,charZ] 
    for i,c in enumerate(mytext):  # i=0 pairs with c = first char in mytext, i = 1 pairs with c = second char, etc
       createCharBlockColour(canvas,x+i*charwidth,y,colour, charactermap[ord(c)-65], LEDpoints)       
          
def Erasepoints(canvas,LEDpoints):
    for p in LEDpoints:
      canvas.delete(p)


