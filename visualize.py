"""
Created on 2/11/20
Marquette Robotics Club
Danny Hudetz

Purpose: read from the hdf5 format and visualize the coordinates mapped nearest
         to user input
"""

import numpy as math
import pygame
import matplotlib
import matplotlib.pyplot as plt
import threading
import h5py as hdf

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY =(100, 100, 100)
LIGHTGRAY=(50,50,50)

pygame.init()

# Set the width and height of the screen [width, height]
WIDTH = 600
HEIGHT = 600
center = pygame.math.Vector2()
center.x = WIDTH/2
center.y = HEIGHT/2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("MegarmModel")

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 15)

# Loop until the user clicks the close button.
done = False

#graphics
scaleFactor = 2.5
lineWidth = 5
doGrid = True
doPlot = True
gridTileSize = 20 #cm
fps = 60

a=31.5
b=31.5
c=7.0

operationHeight=0
operationHeightStore=operationHeight

ar=az=br=bz=cr=cz=frameCount=deg=deg2=endAngle=0
POI=[0,0]
circles=[]

img = pygame.image.load("marquette_robotics.png")
imgScaled = pygame.transform.scale(img, (200, 66))

#todo
def getFile(fileName):
    global a,b,c
    f=None
    try:
        f = hdf.File("simulated\\"+fileName, "r")
        periodSplit=fileName.split('.')
        periodSplit.pop()
        valueSplit=".".join(periodSplit).split('-')
        a=float(valueSplit[0])
        b=float(valueSplit[1])
        c=float(valueSplit[2])
        calculateComponents(0,0,0)
        print("File successfully imported.")
    except:
        print("Check if file exists. Makes sure to inlude \'.hdf5\'")
    return f

def move(f, requestedRadius, requestedZ):
    file = list(f.keys())
    bois = []
    for item in file:
        bois.append(float(item))
    lastDiff = 1000000.0 #this can be any arbitrary value
    for z in bois:
        if requestedZ == z:
            foundZ = z
        else:
            absoluteDiff = float(abs(requestedZ - z))
            if lastDiff > absoluteDiff:
                lastDiff = absoluteDiff
                foundZ = z
    foundZ = str(foundZ)
    dataSet = f[foundZ]
    bois2 = []
    for item in dataSet:
        bois2.append(float(item))
    lastDiff = 1000000.0 #this can also be any arbitrary value
    for r in bois2:
        if requestedRadius == r:
            foundR = r
        else:
            absoluteDiff = float(abs(requestedRadius - r))
            if lastDiff > absoluteDiff:
                lastDiff = absoluteDiff
                foundR = r
    foundR = str(foundR)
    print("Found R: ", foundR)
    print("Found Z: ", foundZ)
    servoAngles = dataSet[foundR]
    print(servoAngles[1], servoAngles[2], servoAngles[3])
    calculateComponents(servoAngles[1],servoAngles[2],servoAngles[3])

def userInputLoop():
    global done
    print("\nMegarm Visualizer")
    f=None
    while not done:
        userInput = input("Import coordinate r z? Type \'help\' for more options: ")
        words=userInput.split()
        if len(words)==2:
            circles=[]
            if(words[0]=='f'):
                f = getFile(words[1])
            elif(f!=None):
                move(f, float(words[0]),float(words[1]))
            else:
                print("File not imported.")
        elif words[0]=="help":
            print("To enter a coordinate just type the r and z.")
            print("Example: 15.0 10.0")
            print("To change hdf5 file reference, type f and the file name.")
            print("Example: f 31.5-31.5-7.0.hdf5")
            print("To quit, type q.")
        elif words[0]=="q":
            done=True
            pygame.quit()
        else:
            print("Improper syntax")

def overlay(t, x, y, color):
    text = font.render(t, True, color, BLACK)

    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)

def drawGrid():
    for i in range(0,int(WIDTH/(scaleFactor*gridTileSize*2))+1):
        gridRight = int(i*(scaleFactor*gridTileSize))+center.x
        gridLeft = center.x-int(i*(scaleFactor*gridTileSize))
        pygame.draw.line(screen, LIGHTGRAY, (gridRight, 0), (gridRight, HEIGHT), 1)
        pygame.draw.line(screen, LIGHTGRAY, (gridLeft, 0), (gridLeft, HEIGHT), 1)

    for j in range(0,int(HEIGHT/(scaleFactor*gridTileSize*2))+1):
        gridDown = int(j*(scaleFactor*gridTileSize))+center.y
        gridUp = center.y-int(j*(scaleFactor*gridTileSize))
        pygame.draw.line(screen, LIGHTGRAY, (0, gridUp), (WIDTH, gridUp), 1)
        pygame.draw.line(screen, LIGHTGRAY, (0, gridDown), (WIDTH, gridDown), 1)

try:
    userThread = threading.Thread(target=userInputLoop, args=())
    userThread.start()
except:
    print("Error: unable to start thread")

def calculateComponents(t1, t2, t3):
    global ar,az,br,bz,cr,cz

    ta = math.deg2rad(t1)
    ar = a*math.cos(ta)
    az = -a*math.sin(ta)

    tb = math.deg2rad(t2-270+t1)
    br = b*math.sin(tb)
    bz = b*math.cos(tb)

    tc = math.deg2rad(t3-(90-(t2-180+t1)))
    cr = c*math.sin(tc)
    cz = c*math.cos(tc)

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    frameCount+=1

    screen.fill(BLACK)
    avector = pygame.math.Vector2()
    avector.x = ar*scaleFactor
    avector.y = az*scaleFactor
    bvector = pygame.math.Vector2()
    bvector.x = br*scaleFactor
    bvector.y = bz*scaleFactor
    cvector = pygame.math.Vector2()
    cvector.x = cr*scaleFactor
    cvector.y = cz*scaleFactor

    POI = center+avector+bvector+cvector
    for cir in circles:
        pygame.draw.circle(screen, GRAY, [int(cir.x),int(cir.y)], 1)

    if doGrid:
        drawGrid()

    pygame.draw.line(screen, RED, center, center+avector, lineWidth)
    pygame.draw.line(screen, GREEN, center+avector, center+avector+bvector, lineWidth)
    pygame.draw.line(screen, BLUE, center+avector+bvector, POI, lineWidth)

    pygame.draw.circle(screen, WHITE, [int(POI.x),int(POI.y)], 3)
    pygame.draw.circle(screen, WHITE, [int(center.x),int(center.y)], 3)
    pygame.draw.circle(screen, WHITE, [int((center+avector).x),int((center+avector).y)], 3)
    pygame.draw.circle(screen, WHITE, [int((center+avector+bvector).x),int((center+avector+bvector).y)], 3)

    finalRadius = (POI.x-center.x)/scaleFactor
    finalHeight = -(POI.y-center.y)/scaleFactor
    overlay("Grid tile is "+str(gridTileSize)+"cm by "+str(gridTileSize)+"cm", 100, 30, WHITE)
    overlay("Radius: " + str(round(finalRadius,3)) + "cm", 100, 50, WHITE)
    overlay("Height: " + str(round(finalHeight,3)) + "cm", 100, 70, WHITE)
    screen.blit(imgScaled, (WIDTH-200, 0))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
