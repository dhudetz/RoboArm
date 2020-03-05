import h5py as hdf
import array as arr
import numpy as np

f = hdf.File("simulated\\31.0-31.0-7.0.hdf5", "r")
requestedZ = float(input("Enter a 'z':"))
file = list(f.keys())
bois = []
for item in file:
    bois.append(float(item))
lastDiff = 100.0 #this can be any arbitrary value
for z in bois:
    if requestedZ == z:
        foundZ = z
    else:
        absoluteDiff = float(abs(requestedZ - z))
        if lastDiff > absoluteDiff:
            lastDiff = absoluteDiff
            foundZ = z
foundZ = str(foundZ)
print("Found Z: ", foundZ)
dataSet = f[foundZ]
requestedRadius = float(input("Enter a 'r': "))
print("Entered r: "+str(requestedRadius))
bois2 = []
for item in dataSet:
    bois2.append(float(item))
lastDiff = 20.0 #this can also be any arbitrary value
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
servoAngles = dataSet[foundR]
print(servoAngles[1], servoAngles[2], servoAngles[3])
