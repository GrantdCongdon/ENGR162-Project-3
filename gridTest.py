import MazeRobot as robot
import csv
import grovepi as gp

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

"""
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
"""


while (not robot.exitMaze):
    
    if (not robot.getLeftWall()): # left wall does not exist
        if (robot.orientation == 0):
            robot.moveWest()
        elif (robot.orientation == 1):
            robot.moveNorth()
        elif (robot.orientation == 2):
            robot.moveEast()
        else:
            robot.moveSouth()
    elif (robot.getIrHazard()): # ir hazard exists
        if (robot.orientation == 0):
            robot.setMazeValue(robot.coords[0], robot.coords[1] + 1, 2)
            robot.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(robot.irPort), "Hazard X-Coordinate": robot.coords[0]*robot.unitDistance,
                                 "Hazard Y-Coordinate": (robot.coords[1] + 1)*robot.unitDistance})
        elif (robot.orientation == 1):
            robot.setMazeValue(robot.coords[0] + 1, robot.coords[1], 2)
            robot.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(robot.irPort), "Hazard X-Coordinate": (robot.coords[0] + 1)*robot.unitDistance,
                                 "Hazard Y-Coordinate": robot.coords[1]*robot.unitDistance})
        elif (robot.orientation == 2):
            robot.setMazeValue(robot.coords[0], robot.coords[1] - 1, 2)
            robot.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(robot.irPort), "Hazard X-Coordinate": robot.coords[0]*robot.unitDistance,
                                 "Hazard Y-Coordinate": (robot.coords[1] - 1)*robot.unitDistance})
        else:
            robot.setMazeValue(robot.coords[0] - 1, robot.coords[1], 2)
            robot.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(robot.irPort), "Hazard X-Coordinate": (robot.coords[0] - 1)*robot.unitDistance,
                                 "Hazard Y-Coordinate": robot.coords[1]*robot.unitDistance})
        robot.turn(90)
    elif (robot.getMagnetHazard()): # magnet hazard exists
        if (robot.orientation == 0):
            robot.setMazeValue(robot.coords[0], robot.coords[1] + 1, 2)
            robot.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": robot.imu.readMagnet()["z"], "Hazard X-Coordinate": robot.coords[0]*robot.unitDistance,
                                 "Hazard Y-Coordinate": (robot.coords[1] + 1)*robot.unitDistance})
        elif (robot.orientation == 1):
            robot.setMazeValue(robot.coords[0] + 1, robot.coords[1], 2)
            robot.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": robot.imu.readMagnet()["z"], "Hazard X-Coordinate": (robot.coords[0] + 1)*robot.unitDistance,
                                 "Hazard Y-Coordinate": robot.coords[1]*robot.unitDistance})
        elif (robot.orientation == 2):
            robot.setMazeValue(robot.coords[0], robot.coords[1] - 1, 2)
            robot.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": robot.imu.readMagnet()["z"], "Hazard X-Coordinate": robot.coords[0]*robot.unitDistance,
                                 "Hazard Y-Coordinate": (robot.coords[1] - 1)*robot.unitDistance})
        else:
            robot.setMazeValue(robot.coords[0] - 1, robot.coords[1], 2)
            robot.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": robot.imu.readMagnet()["z"], "Hazard X-Coordinate": (robot.coords[0] - 1)*robot.unitDistance,
                                 "Hazard Y-Coordinate": robot.coords[1]*robot.unitDistance})
        robot.turn(90)
    elif (robot.getFrontWall()): # front wall exists
        robot.turn(90)
    else: # left wall exists, no hazards, front wall does not exist
        if (robot.orientation == 0):
            robot.moveNorth()
        elif (robot.orientation == 1):
            robot.moveEast()
        elif (robot.orientation == 2):
            robot.moveSouth()
        elif (robot.orientation == 3):
            robot.moveWest()

# maze exitted
robot.celebrate()


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
