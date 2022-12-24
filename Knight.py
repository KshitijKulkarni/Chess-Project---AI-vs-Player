import chess
import Pathfinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np
import USB_Com_Utils as USB

def SqCoord2SqID(x, y):
    return (x*8)+y

def CheckPath(sq1, sq2, binaricRep):
    grid = Grid(matrix=binaricRep)
    start = grid.node(sq1[0], sq1[1])
    end = grid.node(sq2[0], sq2[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    grid.cleanup()
    pathExists = True
    if(len(path) > 0):
        print("Path Found")
    else:
        print("No Path Found")
        pathExists = False
    print(grid.grid_str(path=path, start=start, end=grid.node(sq2[0], sq2[1])))
    return path, pathExists

def CheckPath2(sq1, sq2, binaricRep):
    grid = Grid(matrix=binaricRep)
    start = grid.node(sq1[0], sq1[1])
    end = grid.node(sq2[0], sq2[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)
    path, runs = finder.find_path(start, end, grid)
    grid.cleanup()
    pathExists = True
    if(len(path) > 0):
        print("Path Found")
    else:
        print("No Path Found")
        pathExists = False
    print(grid.grid_str(path=path, start=start, end=grid.node(sq2[0], sq2[1])))
    return path, pathExists

def ExecutePath(path, usb):
    print("Executing Path")

def GetNeighbors(square, SearchArea):
    neighbors = []
    for i in range(SearchArea):
        neighbors.append((square[0], square[1] + i))
        neighbors.append((square[0], square[1] - i))
        neighbors.append((square[0] + i, square[1]))
        neighbors.append((square[0] - i, square[1]))
        neighbors.append((square[0] + i, square[1] + i))
        neighbors.append((square[0] + i, square[1] - i))
        neighbors.append((square[0] - i, square[1] + i))
        neighbors.append((square[0] - i, square[1] - i))
    newNeighbors = []
    #check if neighbors are in bounds of the board
    for i in range(8 * SearchArea):
        if not (neighbors[i][0] < 0 or neighbors[i][0] > 7 or neighbors[i][1] < 0 or neighbors[i][1] > 7):
            newNeighbors.append(neighbors[i])
    print(newNeighbors)
    return newNeighbors

def PathToArrayOfActualPositions(path, physicalLocations):
    actualPath = []
    for i in range(len(path)):
        actualPath.append(physicalLocations[SqCoord2SqID(path[i][0],path[i][1])])
    return actualPath

def Reverse(lst):
    return [ele for ele in reversed(lst)] #code from https://www.geeksforgeeks.org/python-reversing-list/

def MakeMove(sq1, sq2, chessboard: chess.Board, usb, physicalLocations):
    binaricRep = Pathfinder.ChessboardToMatrix(chessboard)
    path,isPath = CheckPath(sq1, sq2, binaricRep)
    if isPath:
        USB.CPMove(PathToArrayOfActualPositions(path, physicalLocations))
    else:
        print("No Path Found")
        neighboringSqs = GetNeighbors(sq1, 8)
        for i in range(len(neighboringSqs)):
            print(i)
            oldValue = binaricRep[neighboringSqs[i][1]][neighboringSqs[i][0]]
            binaricRep[neighboringSqs[i][1]][neighboringSqs[i][0]] = 1
            currentCoord = neighboringSqs[i]
            path,isPath = CheckPath(sq1, sq2, binaricRep)
            if isPath:
                binaricRep[neighboringSqs[i][1]][neighboringSqs[i][0]] = oldValue
                break
            else: 
                binaricRep[neighboringSqs[i][1]][neighboringSqs[i][0]] = oldValue

        ObstacleSquare = currentCoord
        obstacleNeighbors = GetNeighbors(ObstacleSquare,2)
        for i in range(len(obstacleNeighbors)):
            if obstacleNeighbors[i] != sq1:
                if binaricRep[obstacleNeighbors[i][1]][obstacleNeighbors[i][0]] == 1:
                    binaricRep[ObstacleSquare[1]][ObstacleSquare[0]] = 1
                    binaricRep[obstacleNeighbors[i][1]][obstacleNeighbors[i][0]] = 0
                    path,isPath = CheckPath(sq1, sq2, binaricRep)
                    # ObsPath, isObsPath = CheckPath2(ObstacleSquare, obstacleNeighbors[i], binaricRep)
                    if isPath:
                        ObsTar = obstacleNeighbors[i]
                        break
                    else:
                        binaricRep[ObstacleSquare[1]][ObstacleSquare[0]] = 0
                        binaricRep[obstacleNeighbors[i][1]][obstacleNeighbors[i][0]] = 1
        print(ObsTar)
        USB.MakeMove(physicalLocations[SqCoord2SqID(ObstacleSquare[0], ObstacleSquare[1])], physicalLocations[SqCoord2SqID(ObsTar[0],ObsTar[1])])
        USB.CPMove(PathToArrayOfActualPositions(path, physicalLocations))
        USB.MakeMove(physicalLocations[SqCoord2SqID(ObsTar[0], ObsTar[1])], physicalLocations[SqCoord2SqID(ObstacleSquare[0], ObstacleSquare[1])])

        print(np.matrix(binaricRep))
    print("Making Move; Knight")
    


