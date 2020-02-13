# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 17:51:28 2020

@author: danny
"""

import numpy as math
import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY =(100, 100, 100)

pygame.init()

# Set the width and height of the screen [width, height]
WIDTH = 900
HEIGHT = 700
center = pygame.math.Vector2()
center.x = WIDTH/2
center.y = HEIGHT/2
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("MegarmModel")

clock = pygame.time.Clock()

font = pygame.font.Font('freesansbold.ttf', 15)

# Loop until the user clicks the close button.
done = False

#lenghs of each arm portion
a = 25
b = 35
c = 7

#specified operation
operationHeight = -10
startAngle = 0
endAngle = 60

#graphics
scaleFactor = 5
lineWidth = 5

t1=t2=t3=ar=az=br=bz=cr=cz=count=deg=0
POI=[0,0]

circles=[]

img = pygame.image.load("""marquette robotics.png""")
imgScaled = pygame.transform.scale(img, (200, 66))

def calculateAngles1():
    global t1,t2,t3,deg
    deg += 1
    t1= -(((endAngle-startAngle)/2)*math.cos(math.deg2rad(deg)))+startAngle+(endAngle-startAngle)/2
    if -1 <= (-operationHeight/b)+(a/b)*math.cos(math.deg2rad(90-t1)) <= 1:
        t2= (math.rad2deg(math.arccos((-operationHeight/b)+(a/b)*math.cos(math.deg2rad(90-t1))))-t1-90)
        t3=-t2-t1
        calculateComponents();
    else:
        print("arm can not reach desired point")

def calculateAngles2():
    global t1,t2,t3,deg
    deg += 5
    sineMovement=math.sin(math.deg2rad(deg))
    t1+=sineMovement*1
    t2+=sineMovement*1
    t3+=sineMovement*1
    calculateComponents();

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

def overlay(t, x, y):
    text = font.render(t, True, WHITE, BLACK)

    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    count+=1

    calculateAngles1()

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
    for loc in circles:
        pygame.draw.circle(screen, GRAY, [int(loc.x),int(loc.y)], 1)
    if count<=1000:
        circles.append(POI)
        circles.append(center+avector)

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
    overlay("Radius: " + str(int(finalRadius)) + "cm", 100, 100)
    overlay("Height: " + str(int(finalHeight)) + "cm", 100, 120)
    print("t", t1, " r", finalRadius)
    screen.blit(imgScaled, (WIDTH-200, 0))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
