from cProfile import label
import chess
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

def ChessboardToMatrix(ChessboardInput: chess.Board):
    Chessboard = ChessboardInput
   #create an 8x8 matrix
    matrix = [[0 for x in range(8)] for y in range(8)]
    for i in range(8):
        for j in range(8):
            if(Chessboard.piece_at(chess.square(j, i)) == None):
                matrix[i][j] = 1
            else:
                matrix[i][j] = 0

    return matrix

def SimplifyPath(Path):
    i = 0
    while True:
        if(len(Path) > i+2):
            p1 = Path[i]
            p2 = Path[i+1]
            p3 = Path[i+2]
            if((p2[0] - p1[0])*(p3[1] - p2[1]) - (p2[1] - p1[1])*(p3[0] - p2[0]) == 0): #check if the points are colinear by using this convenient formula: if(x2-x1)(y3-y2) - (y2-y1)(x3-x2) == 0), the points are colinear
                Path.remove(p2)
            else:
                i += 1  
            print(Path)
        else:
            break

                
    return Path

def FindPath(Square, Chessboard, move: chess.Move):
    matrix = ChessboardToMatrix(Chessboard)
    grid = Grid(matrix=matrix)
    #create a shortestPath variable of length 64
    shortestPath = [0 for x in range(131)]
    shortestEndIndex = 0
    diagMovt: DiagonalMovement = DiagonalMovement.never
    for i in range(8):
        start = grid.node(Square[0], Square[1])
        end = grid.node(0, i)
        finder = AStarFinder(diagonal_movement=diagMovt)
        path, runs = finder.find_path(start, end, grid)
        path = SimplifyPath(path)
        grid.cleanup()
        if(len(path) > 0):
            if(len(path) < len(shortestPath)):
                shortestPath = path
                shortestEndIndex = i
    
    if len(shortestPath) == 131: #No Straight path was found
        print("ScanningDiagonally")
        diagMovt = DiagonalMovement.always
        for i in range(8):
            start = grid.node(Square[0], Square[1])
            end = grid.node(0, i)
            finder = AStarFinder(diagonal_movement=diagMovt)
            path, runs = finder.find_path(start, end, grid)
            path = SimplifyPath(path)
            grid.cleanup()
            if(len(path) > 0):
                if(len(path) < len(shortestPath)):
                    shortestPath = path
                    shortestEndIndex = i
        if len(shortestPath) == 131:
            print("NoPathFound")
        else:
            print(Chessboard)
            print(shortestPath)
            print(grid.grid_str(path=shortestPath, start=start, end=grid.node(0, shortestEndIndex)))
            return shortestPath
    else:
        print(Chessboard)
        print(shortestPath)
        print(grid.grid_str(path=shortestPath, start=start, end=grid.node(0, shortestEndIndex)))
        return shortestPath
