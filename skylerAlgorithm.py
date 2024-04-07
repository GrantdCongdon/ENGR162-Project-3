from MazeRobot import MazeRobot
from time import sleep
robot = MazeRobot(MazeRobot.PORT_D, MazeRobot.PORT_A, MazeRobot.PORT_C, 6, 8, 4, MazeRobot.PORT_2, MazeRobot.PORT_3, 2, [0, 0], [6, 6])

while (not robot.exitMaze):
    try:
        if (robot.frontAlignDistance >= robot.wallDetectThreshold and
            robot.rearAlignDistance >= robot.wallDetectThreshold): #no left wall
            robot.turn(-90)
        elif (robot.getIrHazard()): #ir hazard exist
            robot.setHazards()
            robot.turn(180)
        elif (robot.getMagnetHazard()): #magnet hazard exist
            robot.setHazards()
            robot.turn(180)
        elif (robot.getFrontWall()): #front wall exist
            robot.turn(90)
        else:
            robot.moveUnitForward()
    except KeyboardInterrupt:
        robot.stopMotors()
        sleep(0.1)
        robot.reset_all()
        break
map = robot.getMap(37, 0, 40, "cm")
print(map)
map.toCSV("mapSkyler.csv")