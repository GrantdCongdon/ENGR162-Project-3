from MazeRobot import MazeRobot
from time import sleep

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, MazeRobot.PORT_B, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, (3, 0), (5, 6))
    while True:
        d0 = robot.getDistances(0)
        d1 = robot.getDistances(1)
        d2 = robot.getDistances(2)
        print(f"Rear Align: {d0}\tFront Align: {d1}\tFront Sensor: {d2}")

if __name__ == "__main__":
    main()
