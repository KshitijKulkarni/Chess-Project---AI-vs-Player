from itertools import chain
import PhysicalValues as PV
import numpy as np
import matplotlib.pyplot as plt

#Map values from one range to another
def mapVal(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

a1Pos = (1450,0)
a8Pos = (1400,1450)
h1Pos = (0,0)
h8Pos = (0,1450)

#filling in the x values
xVals = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]
for i in range(8):
    xVals[i][0] = mapVal(i,0,7,a1Pos[0],a8Pos[0])

for i in range(8):
    xVals[i][7] = mapVal(i,0,7,h1Pos[0],h8Pos[0])

for vert in range(8):
    for horiz in range(1,7):
        xVals[vert][horiz] = mapVal(horiz,0,7,xVals[vert][0],xVals[vert][7])


#filling in the y values
yVals = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]

for i in range(8):
    yVals[0][i] = mapVal(i,0,7,a1Pos[1],h1Pos[1])

for i in range(8):
    yVals[7][i] = mapVal(i,0,7,a8Pos[1],h8Pos[1])

print (np.array(yVals))

for x in range(8):
    for y in range(1,7):
        yVals[y][x] = mapVal(y,0,7,yVals[0][x],yVals[7][x])

print (np.array(yVals))

MergedValues = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
]
for x in range(8):
    for y in range(8):
        xPos = xVals[x][y]
        yPos = yVals[x][y]
        MergedValues[x][y] = (xPos,yPos)

#flipping the array diagonally to arrange the values
arr = np.array(MergedValues)
arr = np.rot90(arr)
arr = np.fliplr(arr)
arr = np.rot90(np.rot90(arr))
List = list(chain.from_iterable(arr.tolist()))

for i in range(len(List)):
    PV.SetLocation(i,List[i])