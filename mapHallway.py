from MazeRobot import MazeRobot
from time import sleep
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, [0, 0], [6, 6])
    while True:
        try:
            if (not robot.getFrontWall()):
                robot.moveNorth()
            elif (robot.getLeftWall()):
                robot.moveEast()
if __name__ == "__main__":
    main()