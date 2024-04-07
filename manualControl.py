from MazeRobot import MazeRobot

def main():
    robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_3, 2, [0, 0], [6, 6])
    while True:
        print("Enter a command: ")
        command = input()
        if command == "w": robot.moveNorth(wallAlign=False)
        elif command == "s": robot.moveSouth(wallAlign=False)
        elif command == "a": robot.moveWest(wallAlign=False)
        elif command == "d": robot.moveEast(wallAlign=False)
        elif command == "c": robot.depositCargo(wallAlign=False)
        elif command == "s":
            commands = [*input("Enter a sequence of commands: ")]
            for c in commands:
                if c == "w": robot.moveNorth(wallAlign=False)
                elif c == "s": robot.moveSouth(wallAlign=False)
                elif c == "a": robot.moveWest(wallAlign=False)
                elif c == "d": robot.moveEast(wallAlign=False)
                elif c == "c": robot.depositCargo(wallAlign=False)
                else: print("Invalid command")
        elif command == "m": print(robot.getMap(37, 0, 40, "cm"))
        elif command == "q": break
        else: print("Invalid command")

if __name__ == "__main__":
    main()