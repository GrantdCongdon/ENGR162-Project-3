from MazeRobot import MazeRobot
from time import sleep
def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, MazeRobot.PORT_B, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, (14,15), MazeRobot.PORT_1, (2, 0), (5, 7))
    while True:
        try:
            command = input("Enter a command: ")
            if command == "w": robot.moveNorth()
            elif command == "s": robot.moveSouth()
            elif command == "a": robot.moveWest()
            elif command == "d": robot.moveEast()
            elif command == "c": robot.depositCargo()
            elif command == "b": robot.celebrate()
            elif command == "l":
                commands = [*input("Enter a sequence of commands: ")]
                for c in commands:
                    if c == "w": robot.moveNorth()
                    elif c == "s": robot.moveSouth()
                    elif c == "a": robot.moveWest()
                    elif c == "d": robot.moveEast()
                    elif c == "c": robot.depositCargo()
                    elif c == "b": robot.celebrate()
                    elif command == "m":
                        map = robot.getMap(37, 0, 40, "cm")
                        print(map)
                        map.toCSV("map.csv")
                    else: print("Invalid command")
            elif command == "m":
                map = robot.getMap(37, 0, 40, "cm")
                print(map)
                map.toCSV("map.csv")
            elif command == "q": raise KeyboardInterrupt
            else: print("Invalid command")
        
        except robot.Hazard:
            continue

        except KeyboardInterrupt:
            robot.stopMotors()
            sleep(0.1)
            robot.reset_all()
            print("\nProgram Exited")
            break

if __name__ == "__main__":
    main()