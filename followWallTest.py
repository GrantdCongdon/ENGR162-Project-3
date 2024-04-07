from MazeRobot import MazeRobot

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_3, 2, [0, 0], [6, 6])
    robot.moveNorth()
    robot.moveNorth()
    print("Moved North")

if __name__ == "__main__":
    main()