import operator
def SetLocation(Position, Value):
    with open('Coordinates.txt', 'r') as file:
        tempVar = list(file.readlines())
    tempVar[Position] = str(Value).replace("(", "[").replace(")", "]") + "\n"
    with open('Coordinates.txt', 'w') as file:
        file.writelines(tempVar)

globalOffset: tuple = (0, 0)

def GetAllLocations():
    global globalOffset
    with open('Coordinates.txt', 'r') as file:
        tempVar = list(file.readlines())
    #create an array of arrays which is 8x8
    Locations = []
    for y in range(8):
        for x in range(8):
            Locations.append(tuple(map(operator.add, globalOffset, tuple(map(int, str(tempVar[x+8*y]).strip().replace("\n","").replace("[","").replace("]","").split(",")))))) #this adds the global offset to the location. Code from https://stackoverflow.com/a/497894
    return Locations