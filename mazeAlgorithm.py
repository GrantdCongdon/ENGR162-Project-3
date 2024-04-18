from MazeRobot import MazeRobot
from time import sleep
from random import randint

def randomExplore(northWall, eastWall, southWall, westWall, north, south, east, west):
    if north is None: north = 1
    if east is None: east = 1
    if south is None: south = 1
    if west is None: west = 1
    print(f"North: {north}\tEast: {east}\tSouth: {south}\tWest: {west}")
    possibleMoves = ["north", "east", "south", "west"]
    # all possible moves
    if (north == 0 and east == 0 and south == 0 and west == 0):
        return possibleMoves[randint(0, 3)]
    # 3 possible moves
    elif (north == 0 and east == 0 and south == 0 and west != 0):
        return possibleMoves[randint(0, 2)]
    elif (north == 0 and east == 0 and south != 0 and west == 0):
        x = randint(0, 2)
        return possibleMoves[x if x != 2 else 3]
    elif (north == 0 and east != 0 and south == 0 and west == 0):
        x = randint(0, 2)
        return possibleMoves[x if x != 1 else 3]
    elif (north != 0 and east == 0 and south == 0 and west == 0):
        return possibleMoves[randint(1, 3)]
    # 2 possible moves
    elif (north == 0 and east == 0 and south != 0 and west != 0):
        return possibleMoves[randint(0, 1)]
    elif (north == 0 and east != 0 and south == 0 and west != 0):
        x = randint(0, 1)
        return possibleMoves[x if x != 1 else 2]
    elif (north != 0 and east == 0 and south == 0 and west != 0):
        return possibleMoves[randint(1, 2)]
    elif (north != 0 and east != 0 and south == 0 and west == 0):
        return possibleMoves[randint(2, 3)]
    elif (north == 0 and east != 0 and south != 0 and west == 0):
        x = randint(0, 1)
        return possibleMoves[x if x != 0 else 3]
    elif (north != 0 and east == 0 and south != 0 and west == 0):
        x = randint(1, 2)
        return possibleMoves[x if x != 2 else 3]
    # 1 possible move
    elif (north == 0 and east != 0 and south != 0 and west != 0):
        return "north"
    elif (north != 0 and east == 0 and south != 0 and west != 0):
        return "east"
    elif (north != 0 and east != 0 and south == 0 and west != 0):
        return "south"
    elif (north != 0 and east != 0 and south != 0 and west == 0):
        return "west"
    else:
        return None
    
def randomExplore2(northWall, eastWall, southWall, westWall, northMap, eastMap, southMap, westMap):
    moves = []
    if (not northWall): moves.append("north")
    if (not eastWall): moves.append("east")
    if (not southWall): moves.append("south")
    if (not westWall): moves.append("west")

    if (northMap == -1): moves.remove("north")
    if (eastMap == -1): moves.remove("east")
    if (southMap == -1): moves.remove("south")
    if (westMap == -1): moves.remove("west")
    
    if (len(moves) == 0): return None
    elif (len(moves) == 1): return moves[0]
    elif (len(moves) == 2):
        if ("north" in moves and "east" in moves):
            if (northMap == -5): return "north"
            elif (eastMap == -5): return "east"
            elif (northMap == 0 and eastMap != 0): return "north"
            elif (northMap != 0 and eastMap == 0): return "east"
            else: return moves[randint(0, 1)]
        elif ("north" in moves and "south" in moves):
            if (northMap == -5): return "north"
            elif (southMap == -5): return "south"
            elif (northMap == 0 and southMap != 0): return "north"
            elif (northMap != 0 and southMap == 0): return "south"
            else: return moves[randint(0, 1)]
        elif ("north" in moves and "west" in moves):
            if (northMap == -5): return "north"
            elif (westMap == -5): return "west"
            elif (northMap == 0 and westMap != 0): return "north"
            elif (northMap != 0 and westMap == 0): return "west"
            else: return moves[randint(0, 1)]
        elif ("east" in moves and "south" in moves):
            if (eastMap == -5): return "east"
            elif (southMap == -5): return "south"
            elif (eastMap == 0 and southMap != 0): return "east"
            elif (eastMap != 0 and southMap == 0): return "south"
            else: return moves[randint(0, 1)]
        elif ("east" in moves and "west" in moves):
            if (eastMap == -5): return "east"
            elif (westMap == -5): return "west"
            elif (eastMap == 0 and westMap != 0): return "east"
            elif (eastMap != 0 and westMap == 0): return "west"
            else: return moves[randint(0, 1)]
        elif ("south" in moves and "west" in moves):
            if (southMap == -5): return "south"
            elif (westMap == -5): return "west"
            elif (southMap == 0 and westMap != 0): return "south"
            elif (southMap != 0 and westMap == 0): return "west"
            else: return moves[randint(0, 1)]
    elif (len(moves) == 3):
        if ("north" not in moves):
            if (eastMap == -5): return "east"
            elif (southMap == -5): return "south"
            elif (westMap == -5): return "west"
            elif (eastMap == 0 and southMap != 0 and westMap != 0): return "east"
            elif (eastMap != 0 and southMap == 0 and westMap != 0): return "south"
            elif (eastMap != 0 and southMap != 0 and westMap == 0): return "west"
            elif (eastMap == 0 and southMap == 0 and westMap != 0): return moves[randint(0, 1)]
            elif (eastMap == 0 and southMap != 0 and westMap == 0):
                x = randint(0, 1)
                return moves[x if x != 1 else 2]
            elif (eastMap != 0 and southMap == 0 and westMap == 0): return moves[randint(1, 2)]
            else: return moves[randint(0, 2)]
        elif ("east" not in moves):
            if (northMap == -5): return "north"
            elif (southMap == -5): return "south"
            elif (westMap == -5): return "west"
            elif (northMap == 0 and southMap != 0 and westMap != 0): return "north"
            elif (northMap != 0 and southMap == 0 and westMap != 0): return "south"
            elif (northMap != 0 and southMap != 0 and westMap == 0): return "west"
            elif (northMap == 0 and southMap == 0 and westMap != 0): return moves[randint(0, 1)]
            elif (northMap == 0 and southMap != 0 and westMap == 0):
                x = randint(0, 1)
                return moves[x if x != 1 else 2]
            elif (northMap != 0 and southMap == 0 and westMap == 0): return moves[randint(1, 2)]
            else: return moves[randint(0, 2)]
        elif ("south" not in moves):
            if (northMap == -5): return "north"
            elif (eastMap == -5): return "east"
            elif (westMap == -5): return "west"
            elif (northMap == 0 and eastMap != 0 and westMap != 0): return "north"
            elif (northMap != 0 and eastMap == 0 and westMap != 0): return "east"
            elif (northMap != 0 and eastMap != 0 and westMap == 0): return "west"
            elif (northMap == 0 and eastMap == 0 and westMap != 0): return moves[randint(0, 1)]
            elif (northMap == 0 and eastMap != 0 and westMap == 0):
                x = randint(0, 1)
                return moves[x if x != 1 else 2]
            elif (northMap != 0 and eastMap == 0 and westMap == 0): return moves[randint(1, 2)]
            else: return moves[randint(0, 2)]
        elif ("west" not in moves):
            if (northMap == -5): return "north"
            elif (eastMap == -5): return "east"
            elif (southMap == -5): return "south"
            elif (northMap == 0 and eastMap != 0 and southMap != 0): return "north"
            elif (northMap != 0 and eastMap == 0 and southMap != 0): return "east"
            elif (northMap != 0 and eastMap != 0 and southMap == 0): return "south"
            elif (northMap == 0 and eastMap == 0 and southMap != 0): return moves[randint(0, 1)]
            elif (northMap == 0 and eastMap != 0 and southMap == 0):
                x = randint(0, 1)
                return moves[x if x != 1 else 2]
            elif (northMap != 0 and eastMap == 0 and southMap == 0): return moves[randint(1, 2)]
            else: return moves[randint(0, 2)]
    elif (len(moves) == 4):
        if (northMap == -5): return "north"
        elif (eastMap == -5): return "east"
        elif (southMap == -5): return "south"
        elif (westMap == -5): return "west"
        elif (northMap == 0 and eastMap != 0 and southMap != 0 and westMap != 0): return "north"
        elif (northMap != 0 and eastMap == 0 and southMap != 0 and westMap != 0): return "east"
        elif (northMap != 0 and eastMap != 0 and southMap == 0 and westMap != 0): return "south"
        elif (northMap != 0 and eastMap != 0 and southMap != 0 and westMap == 0): return "west"
        elif (northMap == 0 and eastMap == 0 and southMap != 0 and westMap != 0): return moves[randint(0, 1)]
        elif (northMap == 0 and eastMap != 0 and southMap == 0 and westMap != 0):
            x = randint(0, 1)
            return moves[x if x != 1 else 2]
        elif (northMap == 0 and eastMap != 0 and southMap != 0 and westMap == 0):
            x = randint(0, 1)
            return moves[x if x != 0 else 3]
        elif (northMap != 0 and eastMap == 0 and southMap == 0 and westMap != 0): return moves[randint(1, 2)]
        elif (northMap != 0 and eastMap == 0 and southMap != 0 and westMap == 0):
            x = randint(1, 2)
            return moves[x if x != 2 else 3]
        elif (northMap != 0 and eastMap != 0 and southMap == 0 and westMap == 0): return moves[randint(2, 3)]
        elif (northMap == 0 and eastMap == 0 and southMap == 0 and westMap != 0): return moves[randint(0, 2)]
        elif (northMap == 0 and eastMap == 0 and southMap != 0 and westMap == 0):
            x = randint(0, 2)
            return moves[x if x != 1 else 3]
        elif (northMap == 0 and eastMap != 0 and southMap == 0 and westMap == 0):
            x = randint(0, 2)
            return moves[x if x != 0 else 3]
        elif (northMap != 0 and eastMap == 0 and southMap == 0 and westMap == 0): return moves[randint(1, 3)]
        else: return moves[randint(0, 3)]


def rankedExplore(north, east, south, west):
    if north is None: north = 1
    if east is None: east = 1
    if south is None: south = 1
    if west is None: west = 1
    possibleMoves = ["north", "east", "south", "west"]
    # all possible moves
    return
    

bestMove = randomExplore2

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, [1, 0], (3, 7))
    northHazard = False
    eastHazard = False
    southHazard = False
    westHazard = False
    print(f"North: {0}\tEast: {1}\tSouth: {1}\tWest: {1}")
    print(f"X-coord: {robot.location[0]}\tY-coord: {robot.location[1]}")
    print("north")
    sleep(1)
    robot.moveNorth(wallAlign=False)
    while (not robot.exitedMaze):
        try:
            # get the walls around the robot
            northWall = robot.getNorthWall()
            eastWall = robot.getEastWall()
            southWall = robot.getSouthWall()
            westWall = robot.getWestWall()

            # get the values of the surrounding cells
            try:  northMapValue = robot.getMazeValue(robot.location[0], robot.location[1]+1)
            except IndexError: northMapValue = None
            try:  eastMapValue = robot.getMazeValue(robot.location[0]+1, robot.location[1])
            except IndexError: eastMapValue = None
            try:  southMapValue = robot.getMazeValue(robot.location[0], robot.location[1]-1)
            except IndexError: southMapValue = None
            try:  westMapValue = robot.getMazeValue(robot.location[0]-1, robot.location[1])
            except IndexError: westMapValue = None

            northMapValue = northMapValue if not northHazard else None
            eastMapValue = eastMapValue if not eastHazard else None
            southMapValue = southMapValue if not southHazard else None
            westMapValue = westMapValue if not westHazard else None

            print(f"North Wall: {northWall}\tEast Wall: {eastWall}\tSouth Wall: {southWall}\tWest Wall: {westWall}")
            print(f"North Map: {northMapValue}\tEast Map: {eastMapValue}\tSouth Map: {southMapValue}\tWest Map:{westMapValue}")

            # get the best move
            move = bestMove(northWall, eastWall, southWall, westWall, northMapValue, eastMapValue, southMapValue, westMapValue)
            print(f"X-coord: {robot.location[0]}\tY-coord: {robot.location[1]}")
            print(move)

            if (move == "north"):
                try: robot.moveNorth()
                except robot.Hazard: northMapValue = True
            elif (move == "east"):
                try: robot.moveEast()
                except robot.Hazard: eastMapValue = True
            elif (move == "south"):
                try: robot.moveSouth()
                except robot.Hazard: southMapValue = True
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