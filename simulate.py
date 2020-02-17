"""
Created on 2/17/20
Marquette Robotics Club
Danny Hudetz

Purpose: simulate and map the possible movements of a robotic arm with a given
         segment lengths
"""

import numpy as math
import time as t
# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 20, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

print("Please enter the segment lengths you want to simulate:")
a=input("Shoulder to elbow (cm)? ")
b=input("Elbow to wrist (cm)? ")
c=input("Wrist to POI (cm)? ")
resolution=input("Resolution (cm per pixel)? ")

print("Simulating...")
for i in range(0,50):
    printProgressBar(i,50)
    t.sleep(.1)
