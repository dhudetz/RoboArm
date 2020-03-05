"""
Created on 2/17/20
Marquette Robotics Club
Danny Hudetz

Purpose: simulate and map the possible movements of a robotic arm with a given
         segment lengths
"""
import numpy as math
from datetime import datetime
import h5py as hdf
# Print iterations progress

a=b=c=zResolution=angleResolution=0

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 20, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

def getAngleRange(operationHeight):
    endAngle=startAngle=0
    if a<abs(operationHeight):
        if operationHeight>0:
            operationHeight=a
            #print("max height reached")
        else:
            operationHeight=-a
            #print("min height reached")
    if b>a and operationHeight>=0:
        endAngle=180
    else:
        if a>b+operationHeight and a!=0:
            endAngle=math.rad2deg(math.arcsin((b+operationHeight)/a))
        elif a>=abs(operationHeight-b) and a!=0:
            endAngle=-math.rad2deg(math.arcsin((operationHeight-b)/a))
        if a+b>operationHeight>0:
            endAngle=180-endAngle
    startAngle = math.rad2deg(math.arcsin(operationHeight/a))
    return ((startAngle,endAngle))

def calculateServoAngles(operationHeight, t1, startAngle, endAngle):
    t2=t3=0
    #t1= -(((endAngle-startAngle)/2)*a)+startAngle+(endAngle-startAngle)/2
    if -1 <= (-operationHeight/b)+(a/b)*math.sin(math.deg2rad(t1)) <= 1:
        t2=(math.rad2deg(math.arccos((-operationHeight/b)+(a/b)*math.sin(math.deg2rad(t1))))-t1-90)
        t3=-t2-t1
    return(t1, t2, t3)

def getRadius(t1,t2,t3,operationHeight):
    ar = a*math.cos(math.deg2rad(t1))
    br = math.sqrt(b**2-(a*math.sin(math.deg2rad(t1))-operationHeight)**2)
    cr = c
    return ar+br+cr

def generate(aLen,bLen,cLen,zRes,aRes):
    global a,b,c,zResolution,angleResolution
    a=aLen
    b=bLen
    c=cLen
    zResolution=zRes
    angleResolution=aRes
    f = hdf.File("simulated\\"+str(a)+"-"+str(b)+"-"+str(c)+".hdf5", "w")
    zValues=math.arange(-a,a,zResolution)
    zCount=0

    for z in zValues:
        printProgressBar(zCount, len(zValues)-1)
        angles=getAngleRange(z)
        startAngle = angles[0]
        endAngle = angles[1]
        try:
            grp = f.create_group(str(round(z,2)))
            angles=math.arange(startAngle, endAngle, angleResolution)

            for ang in math.arange(-1,1,(2*angleResolution)/(endAngle-startAngle)):
                (shoulder,elbow,wrist)=calculateServoAngles(z,ang,startAngle,endAngle)
                radius=getRadius(shoulder,elbow,wrist,z)
                try:
                    grp.create_dataset(str(round(radius, 8)), data=[radius, shoulder, elbow, wrist])
                except:
                    print("Failed radius data generation...")
                    break
        except:
            print("Failed z group generation...")
        zCount+=1
    f.close()
