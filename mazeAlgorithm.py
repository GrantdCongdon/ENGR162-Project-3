from MazeRobot import MazeRobot
from time import sleep

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, [0, 0], [6, 6])
    while (not robot.exitedMaze):
        try:
            if (not robot.getNorthWall()):
                
        except KeyboardInterrupt:
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            break