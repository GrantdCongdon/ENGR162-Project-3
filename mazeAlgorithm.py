from MazeRobot import MazeRobot
from time import sleep
from random import randint

def randomExplore(north, east, south, west):
    if north is None: north = 1
    if east is None: east = 1
    if south is None: south = 1
    if west is None: west = 1
    possibleMoves = ["north", "east", "south", "west"]
    # all possible moves
    if (north == 0 and east == 0 and south == 0 and west == 0):
        return possibleMoves[randint(0, 3)]
    # 3 possible moves
    elif (north == 0 and east == 0 and south == 0 and west == 1):
        return possibleMoves[randint(0, 2)]
    elif (north == 0 and east == 0 and south == 1 and west == 0):
        x = randint(0, 2)
        return possibleMoves[x if x != 2 else 3]
    elif (north == 0 and east == 1 and south == 0 and west == 0):
        x = randint(0, 2)
        return possibleMoves[x if x != 1 else 3]
    elif (north == 1 and east == 0 and south == 0 and west == 0):
        return possibleMoves[randint(1, 3)]
    # 2 possible moves
    elif (north == 0 and east == 0 and south == 1 and west == 1):
        return possibleMoves[randint(0, 1)]
    elif (north == 0 and east == 1 and south == 0 and west == 1):
        x = randint(0, 1)
        return possibleMoves[x if x != 1 else 2]
    elif (north == 1 and east == 0 and south == 0 and west == 1):
        return possibleMoves[randint(1, 2)]
    elif (north == 1 and east == 1 and south == 0 and west == 0):
        return possibleMoves[randint(2, 3)]
    elif (north == 0 and east == 1 and south == 1 and west == 0):
        x = randint(0, 1)
        return possibleMoves[x if x != 0 else 3]
    elif (north == 1 and east == 0 and south == 1 and west == 0):
        x = randint(1, 2)
        return possibleMoves[x if x != 2 else 3]
    # 1 possible move
    elif (north == 0 and east == 1 and south == 1 and west == 1):
        return "north"
    elif (north == 1 and east == 0 and south == 1 and west == 1):
        return "east"
    elif (north == 1 and east == 1 and south == 0 and west == 1):
        return "south"
    elif (north == 1 and east == 1 and south == 1 and west == 0):
        return "west"
    else:
        return None

bestMove = randomExplore

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, [0, 0], [6, 6])
    northHazard = False
    eastHazard = False
    southHazard = False
    westHazard = False
    while (not robot.exitedMaze):
        try:
            # get the values of the surrounding cells
            try:  northMapValue = robot.getMazeValue(robot.location[0], robot.location[1]+1)
            except IndexError: northMapValue = None
            try:  eastMapValue = robot.getMazeValue(robot.location[0]+1, robot.location[1])
            except IndexError: eastMapValue = None
            try:  southMathValue = robot.getMazeValue(robot.location[0], robot.location[1]-1)
            except IndexError: southMathValue = None
            try:  westMapValue = robot.getMazeValue(robot.location[0]-1, robot.location[1])
            except IndexError: westMapValue = None

            northMapValue = northMapValue if not robot.getNorthWall() else None
            eastMapValue = eastMapValue if not robot.getEastWall() else None
            southMathValue = southMathValue if not robot.getSouthWall() else None
            westMapValue = westMapValue if not robot.getWestWall() else None

            northMapValue = northMapValue if not northHazard else None
            eastMapValue = eastMapValue if not eastHazard else None
            southMathValue = southMathValue if not southHazard else None
            westMapValue = westMapValue if not westHazard else None

            # get the best move
            move = bestMove(northMapValue, eastMapValue, southMathValue, westMapValue)
            
            print(move)

            if (move == "north"):
                try: robot.moveNorth()
                except robot.Hazard: northMapValue = True
            elif (move == "east"):
                try: robot.moveEast()
                except robot.Hazard: eastMapValue = True
            elif (move == "south"):
                try: robot.moveSouth()
                except robot.Hazard: southMathValue = True
            elif (move == "west"):
                try: robot.moveWest()
                except robot.Hazard: westMapValue = True

            if (robot.exitedMaze):
                robot.moveUnitForward(wallAlign=False)
                robot.depositCargo()
                robot.celebrate()
                break

        except KeyboardInterrupt:
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            break
    robot.resetAll()
    return

if __name__ == "__main__":
    main()