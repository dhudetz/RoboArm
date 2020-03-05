import h5py as hdf
import array as arr
import numpy as np

f = hdf.File("simulated\\31.0-31.0-7.0.hdf5", "r")

zrinputs = float(input("Enter a 'z':"))
print("Entered z: "+str(zrinputs)) #remove later
file = list(f.keys())
bois = []
for item in file:
    bois.append(float(item))
loopCheckVar = 100.0 #this can be any arbitrary value
for z in bois:
    if zrinputs == z:
        break
    else:
        absoluteDiff = float(abs(zrinputs - z))
        if loopCheckVar > absoluteDiff:
            loopCheckVar = absoluteDiff
            foundZ = z
foundZ = str(foundZ)
dataSet = f[foundZ]
radius = float(input("Enter a 'r': "))
print("Entered r: "+str(radius))
bois2 = []
for item in dataSet:
    bois2.append(float(item))
loopCheckVar = 20.0 #this can also be any arbitrary value
for r in bois2:
    if radius == r:
        break
    else:
        absoluteDiff = float(abs(radius - r))
        if loopCheckVar > absoluteDiff:
            loopCheckVar = absoluteDiff
            foundR = r
foundR = str(foundR)
servoAngles = dataSet[foundR]
print(servoAngles[1])
