from MazeRobot import MazeRobot
from time import sleep
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, [0, 0], [6, 6])
    while True:
        try:
            command = input("Enter a command: ")
            if command == "w": robot.moveNorth(wallAlign=True)
            elif command == "s": robot.moveSouth(wallAlign=False)
            elif command == "a": robot.moveWest(wallAlign=False)
            elif command == "d": robot.moveEast(wallAlign=False)
            elif command == "c": robot.depositCargo()
            elif command == "s":
                commands = [*input("Enter a sequence of commands: ")]
                for c in commands:
                    if c == "w": robot.moveNorth(wallAlign=False)
                    elif c == "s": robot.moveSouth(wallAlign=False)
                    elif c == "a": robot.moveWest(wallAlign=False)
                    elif c == "d": robot.moveEast(wallAlign=False)
                    elif c == "c": robot.depositCargo()
                    else: print("Invalid command")
            elif command == "m":
                map = robot.getMap(37, 0, 40, "cm")
                print(map)
                map.toCSV("map.csv")
            elif command == "q": raise KeyboardInterrupt
            else: print("Invalid command")
        
        except KeyboardInterrupt:
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            print("\nProgram Exited")
            break

if __name__ == "__main__":
    main()