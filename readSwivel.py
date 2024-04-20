from MazeRobot import MazeRobot
from time import sleep
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, MazeRobot.PORT_B, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, (3, 0), (5, 6))
    while True:
        print(f"Front Distance: {robot.getDistances(2)}")
        sleep(1)
        print(f"Right Distance: {robot.getDistances(3)}")
        sleep(1)
if __name__ == "__main__":
    main()