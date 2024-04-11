import MazeRobot as robot
import csv

hazardFile = "team37_hazards.csv"
mapFile = "team37_map.csv"

# Declare grid size, start position, end position, and starting position
gridSize = [6, 6]
start = [0, 0]
end = [3, 0]
orientation = 0 # 0 NORTH, 1 EAST, 2 SOUTH, 3 WEST

# Inputs?
mapNum = 0

printList = []
hazardList = []
position = start

# Establishes matrices for grid coordinates and status
grid = [gridSize[0] - 1, gridSize[1] - 1]
gridCoordinates = [[column for column in range(gridSize[1])] for row in
                   range(gridSize[0])]
gridStatus = [[column for column in range(gridSize[1])] for row in
              range(gridSize[0])]

# Establishes coordinates and resets grid status
for row in range(0, gridSize[0]):
    printList.append('')
    for columnNum in range(gridSize[1]):
        column = grid[1] - columnNum
        gridCoordinates[row][columnNum] = [row, column]
        gridStatus[row][column] = 0
# Starting square = explored
gridStatus[grid[0] - start[0]][start[1]] = 5

# Grid status: ONLY USES 0 AND 1 ATM
# 0 Not part of path taken
# 1 Path GEARS took
# 2 Heat
# 3 Magnet
# 4 Exit
# 5 Origin
#-----------------
# -1 Wall
# -2 Intersection
#-----------------

#distanceX = end[0] - start[0]
#distanceY = end[1] - start[1]



def printResults(x):
    writeList = [["Team: 37"], ["Map: " + str(mapNum)], ["Unit Length: 10"],
                 ["Unit: cm"], ['Origin: (0, 0)'], ["Notes: any notes we may have"]]
    print(writeList)
    
    if (x == 0):
        for i in range(0, gridSize[0]):
            for j in range(gridSize[1]):
                printList[i] = printList[i] + str(gridStatus[i][j])
                if (j != (gridSize[1] - 1)):
                    printList[i] = printList[i] + ","
                    
        print("Team: 37")
        print("Map: " + str(mapNum))
        print("Unit Length: 10")
        print("Unit: cm")
        print("Origin: (" + str(start[0]) + "," + str(start[1]) + ")")
        print("Notes: any notes we may have")
        
        for i in range(len(printList)):
            print(printList[i])
    else:
        with open(mapFile, 'w+', newline = '') as file:
            write = csv.writer(file)
        #write = csv.writer(open(mapFile, 'w+', newline = ''), quoting=csv.QUOTE_NONE)
            for i in range(len(writeList)):
                write.writerow(writeList[i])
        with open(mapFile, 'a', newline = '') as file:
            write = csv.writer(file)
            write.writerows(gridStatus)
        with open(hazardFile, 'a', newline = '') as file:
            write = csv.writer(file)
            write.writerows(hazardList)

def checkUp():
    if (gridStatus[grid[0] - position[0]][position[1] + 1] == 1):
        orientation = 0 #rotate up
        position[1] = position[1] + 1# move up
        #distanceY = end[1] - position[1]
    elif (gridStatus[grid[0] - position[0]][position[1] + 1] == 0):
        orientation = 0 #rotate up
        #move up while detecting, dont update position til fully moved
        gridStatus[grid[0] - position[0]][position[1] + 1] = 1
        #distanceY = end[1] - position[1]
    #return(orientation, distanceY)

def checkRight():
    if (gridStatus[grid[0] - position[0] + 1][position[1]] == 1):
        orientation = 1 #rotate right
        position[0] = position[0] + 1 #move right
        #distanceX = end[0] - position[0]
    elif (gridStatus[grid[0] - position[0] + 1][position[1]] == 0):
        orientation = 1 #rotate right
        #move right while detecting, dont update til fully moved

def checkDown():
    if (gridStatus[grid[0] - position[0] - 1][position[1]] == 1):
        orientation = 3 #rotate left
        position[0] = position[0] - 1 #move left
        #distanceX = end[0] - position[0]
    elif (gridStatus[grid[0] - position[0] - 1][position[1]] == 0):
        orientation = 3 #rotate left
        #move left while detecting, dont update til fully moved

def checkLeft():
    if (gridStatus[grid[0] - position[0]][position[1] - 1] == 1):
        orientation = 2 #rotate down
        position[1] = position[1] - 1# move down
        #distanceY = end[1] - position[1]
    elif (gridStatus[grid[0] - position[0]][position[1] - 1] == 0):
        orientation = 2 #rotate down
        #move down while detecting, dont update position til fully moved
        gridStatus[grid[0] - position[0]][position[1] - 1] = 1
        #distanceY = end[1] - position[1]
    
printResults(1)

while (not robot.exitMaze):
    if (robot.frontAlignDistance >= robot.wallDetectThreshold and
        robot.rearAlignDistance >= robot.wallDetectThreshold): #no left wall
        robot.turn(-90)
    elif (robot.getIrHazard()): #ir hazard exist
        robot.setHazards()
        robot.turn(180)
    elif (robot.getMagnetHazard()): #magnet hazard exist
        robot.setHazards()
        robot.turn(180)
    elif (robot.getFrontWall()): #front wall exist
        robot.turn(90)
    else:
        robot.moveUnitForward()

"""while not (distanceX == 0 and distanceY == 0):
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
        """
