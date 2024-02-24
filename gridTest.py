gridSize = [4, 4]
start = [0, 0]
end = [3, 0]
orientation = 0

position = start

grid = [gridSize[0] - 1, gridSize[1] - 1]
gridCoordinates = [[column for column in range(gridSize[1])] for row in
                   range(gridSize[0])]
gridStatus = [[column for column in range(gridSize[1])] for row in
              range(gridSize[0])]
gridStatus[grid[0] - start[0]][start[1]] = 1

for row in range(0, gridSize[0]):
    for columnNum in range(gridSize[1]):
        column = grid[1] - columnNum
        gridCoordinates[row][columnNum] = [row, column]
        gridStatus[row][column] = 0

distanceX = end[0] - start[0]
distanceY = end[1] - start[1]

def checkUp():
    if (gridStatus[grid[0] - position[0]][position[1] + 1] == 1):
        orientation = 0 #rotate up
        position[1] = position[1] + 1# move up
        distanceY = end[1] - position[1]
    elif (gridStatus[grid[0] - position[0]][position[1] + 1] == 0):
        orientation = 0 #rotate up
        #move up while detecting, dont update position til fully moved
        gridStatus[grid[0] - position[0]][position[1] + 1] = 1
        distanceY = end[1] - position[1]
    #return(orientation, distanceY)

def checkRight():
    if (gridStatus[grid[0] - position[0] + 1][position[1]] == 1):
        orientation = 1 #rotate right
        position[0] = position[0] + 1 #move right
        distanceX = end[0] - position[0]
    elif (gridStatus[grid[0] - position[0] + 1][position[1]] == 0):
        orientation = 1 #rotate right
        #move right while detecting, dont update til fully moved

def checkDown():
    if (gridStatus[grid[0] - position[0] - 1][position[1]] == 1):
        orientation = 3 #rotate left
        position[0] = position[0] - 1 #move left
        distanceX = end[0] - position[0]
    elif (gridStatus[grid[0] - position[0] - 1][position[1]] == 0):
        orientation = 3 #rotate left
        #move left while detecting, dont update til fully moved

def checkLeft():
    if (gridStatus[grid[0] - position[0]][position[1] - 1] == 1):
        orientation = 2 #rotate down
        position[1] = position[1] - 1# move down
        distanceY = end[1] - position[1]
    elif (gridStatus[grid[0] - position[0]][position[1] - 1] == 0):
        orientation = 2 #rotate down
        #move down while detecting, dont update position til fully moved
        gridStatus[grid[0] - position[0]][position[1] - 1] = 1
        distanceY = end[1] - position[1]
    
while not (distanceX == 0 and distanceY == 0):
    if (distanceY > 0):
        if ((gridStatus[grid[0] - position[0]][position[1] + 1] == 0) or
        (gridStatus[grid[0] - position[0]][position[1] + 1] == 1)):
            checkUp()
        else:
            if ((gridStatus[grid[0] - position[0] + 1][position[1]] == 0) or
            (gridStatus[grid[0] - position[0] + 1][position[1]] == 1)):
                checkRight()
            else:
                if ((gridStatus[grid[0] - position[0] - 1][position[1]] == 0)
                or (gridStatus[grid[0] - position[0] - 1][position[1]] == 1)):
                    checkDown()
                else:
                    checkLeft()
    if (distanceX > 0):
        if ((gridStatus[grid[0] - position[0] + 1][position[1]] == 0) or
        (gridStatus[grid[0] - position[0] + 1][position[1]] == 1)):
            checkRight()
        else:
            if ((gridStatus[grid[0] - position[0]][position[1] + 1] == 0) or
            (gridStatus[grid[0] - position[0]][position[1] + 1] == 1)):
                checkUp()
            else:
                if ((gridStatus[grid[0] - position[0] - 1][position[1]] == 0)
                or (gridStatus[grid[0] - position[0] - 1][position[1]] == 1)):
                    checkDown()
                else:
                    checkLeft()
    if (distanceY < 0):
        if ((gridStatus[grid[0] - position[0]][position[1] - 1] == 0) or
        (gridStatus[grid[0] - position[0]][position[1] - 1] == 1)):
            checkDown()
        else:
            if ((gridStatus[grid[0] - position[0] + 1][position[1]] == 0) or
            (gridStatus[grid[0] - position[0] + 1][position[1]] == 1)):
                checkRight()
            else:
                if ((gridStatus[grid[0] - position[0] + 1][position[1]] == 0)
                or (gridStatus[grid[0] - position[0] + 1][position[1]] == 1)):
                    checkUp()
                else:
                    checkLeft()
    if (distanceX < 0):
        if ((gridStatus[grid[0] - position[0] - 1][position[1]] == 0) or
        (gridStatus[grid[0] - position[0] - 1][position[1]] == 1)):
            checkLeft()
        else:
            if ((gridStatus[grid[0] - position[0]][position[1] + 1] == 0) or
            (gridStatus[grid[0] - position[0]][position[1] + 1] == 1)):
                checkUp()
            else:
                if ((gridStatus[grid[0] - position[0] - 1][position[1]] == 0)
                or (gridStatus[grid[0] - position[0] - 1][position[1]] == 1)):
                    checkDown()
                else:
                    checkRight()
        