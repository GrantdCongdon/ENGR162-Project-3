from MazeRobot import MazeRobot
from time import sleep

#(0,1), (0,0), (2, 0), (2,2)
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, [0, 0], [6, 6])
    deadEnd = False
    while True:
        try:
            if (not robot.getFrontWall() and not deadEnd):
                robot.moveNorth()
            elif (robot.getLeftWall() and not robot.getRightWall()):
                robot.moveEast()
            elif (robot.getRightWall() and not robot.getLeftWall()):
                robot.moveWest()
            elif (robot.getRightWall() and robot.getLeftWall()):
                deadEnd = True
                robot.moveSouth()
        except KeyboardInterrupt:
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            break
    map = robot.getMap()
    print(map)
    map.toCSV("mapHallway.csv")
if __name__ == "__main__":
    main()