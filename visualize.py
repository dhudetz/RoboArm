# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:51:28 2020

@author: danny
"""

import numpy as math
import pygame
import matplotlib
import matplotlib.pyplot as plt
import threading

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
cyclesPerSec=.5
operationHeightStore=operationHeight

t1=t2=t3=ar=az=br=bz=cr=cz=frameCount=deg=deg2=endAngle=0
POI=[0,0]
circles=[]

img = pygame.image.load("marquette robotics.png")
imgScaled = pygame.transform.scale(img, (200, 66))

#todo
def importFile():
    #importFile
    #preload the data? maybe at least the z names and radius names
    print("Nuthing")

#note: has to move only to a valid coordinate
def move(coordinate):
    (radius,height)=coordinate
    #check validity
    #find closest point on the map
    #move angles in half sine wave to needed position

def userInputLoop():
    global a,b,c,operationHeight,cyclesPerSec,done,scaleFactor,endAngle,startAngle,circles,gridTileSize
    print("\nSyntax to change coordinate: \"\"\nEnter q to quit.")
    while not done:
        userInput = input("Import coordinate? ")
        words=userInput.split()
        if len(words)==2:
            circles=[]
            coord=(words[0],words[1])
            move(coord)
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

def calculateComponents():
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
    print("%s %s %s" % (ar, br, cr))

goingUp = True
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

    #if frameCount<fps/cyclesPerSec:
#    if frameCount<1000:
#        circles.append(POI)
#        circles.append(center+avector)

    pygame.draw.line(screen, RED, center, center+avector, lineWidth)
    pygame.draw.line(screen, GREEN, center+avector, center+avector+bvector, lineWidth)
    pygame.draw.line(screen, BLUE, center+avector+bvector, POI, lineWidth)
    #pygame.draw.line(screen, GRAY, center, POI, 1)

    pygame.draw.circle(screen, WHITE, [int(POI.x),int(POI.y)], 3)
    pygame.draw.circle(screen, WHITE, [int(center.x),int(center.y)], 3)
    pygame.draw.circle(screen, WHITE, [int((center+avector).x),int((center+avector).y)], 3)
    pygame.draw.circle(screen, WHITE, [int((center+avector+bvector).x),int((center+avector+bvector).y)], 3)

    finalRadius = (POI.x-center.x)/scaleFactor
    finalHeight = -(POI.y-center.y)/scaleFactor
    overlay("Grid tile is "+str(gridTileSize)+"cm by "+str(gridTileSize)+"cm", 100, 30, WHITE)
    overlay("Radius: " + str(int(finalRadius)) + "cm", 100, 50, WHITE)
    overlay("Height: " + str(int(finalHeight)) + "cm", 100, 70, WHITE)
    overlay("Angle 1: " + str(int(t1)) + "deg", 100, 90, RED)
    overlay("Angle 2: " + str(int(t2)) + "deg", 100, 110, GREEN)
    overlay("Angle 3: " + str(int(t3)) + "deg", 100, 130, BLUE)
#    print("t", t1, " r", finalRadius)
    screen.blit(imgScaled, (WIDTH-200, 0))

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
