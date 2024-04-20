from MazeRobot import MazeRobot
from time import sleep
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, MazeRobot.PORT_B, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, MazeRobot.PORT_1, (3, 0), (5, 6))
    while True:
        try:
            print("Aligning robot...")
            robot.align(1)
            print("Robot aligned")
            sleep(3)
        except KeyboardInterrupt:
            robot.swivel(0)
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            print("\nProgram Exited")
            break

if __name__ == "__main__":
    main()