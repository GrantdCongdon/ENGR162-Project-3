#import necessary libraries
import grovepi as gp
from brickpi3 import BrickPi3, SensorError
from MPU9250 import MPU9250
from time import sleep

# class that covers all the aspects of the ENGR161/162 robot
class MazeRobot(BrickPi3, MPU9250, gp):
    class Map:
        def __init__(self, teamNumber, mapNumber, unitLength, unit, origin, map, notes=""):
            self.teamNumber = teamNumber
            self.mapNumber = mapNumber
            self.unitLength = unitLength
            self.unit = unit
            self.notes = notes
            self.origin = origin
            self.map = map
        
        def __str__(self):
            basicInfo = f"Team Number: {self.teamNumber}\nMap Number: {self.mapNumber}\nUnit Length: {self.unitLength}\nUnit: {self.unit}\nOrigin: {self.origin}\nNotes: {self.notes}\n"
            mapInfo = ""
            for row in self.map:
                for cell in row:
                    mapInfo += f"{cell}, "
                mapInfo += "\n"
            return basicInfo + mapInfo
    # defines the default motor speed to go forward at
    motorSpeed = -200
    
    # defines the default proportional gain for driving and turning
    driveProportionalGain = 0.5
    turnProportionalGain = 0.5
    wallAlignProportionalGain = 0.5
    
    # defines the default threshold for the IR sensor when a hazard is present
    irHazardThreshold = 25
    
    # defines the default threshold for the magnet sensor when hazard is present
    magnetHazardThreshold = 50

    # encoder distance for 1 unit
    encoderDistance = 1056

    # default distance for wall alignment
    wallDistance=10

    # default threshold for the wall detection
    wallDetectThreshold = 15

    # define whether in the maze or not
    exitedMaze = False

    # intakes the default ports for the motors, ultrasonics, gyro, and IR sensor
    def __init__(self, rightMotorPort, leftMotorPort,
                 frontAlignDistanceSensorPort, rearAlignDistanceSensorPort,
                 frontDistanceSensorPort, gyroPort, irPort, coords, mazeSize,
                 orientation=0):
        # initializes the brickpi3, MPU9250, and grovepi
        super().__init__()
        
        # takes parameters and assigns them to the class
        self.rightMotorPort = rightMotorPort
        self.leftMotorPort = leftMotorPort
        self.frontAlignDistanceSensorPort = frontAlignDistanceSensorPort
        self.rearAlignDistanceSensorPort = rearAlignDistanceSensorPort
        self.frontDistanceSensorPort = frontDistanceSensorPort
        self.gyroPort = gyroPort
        self.irPort = irPort
        self.startCoords = coords
        self.coords = coords
        self.orientation = orientation
        self.maze = [[0 for _ in range(mazeSize[0])] for _ in range(mazeSize[1])]
        self.setMazeValue(self.startCoords[0], self.startCoords[1], 5)
        
        # configure gyro sensor
        self.set_sensor_type(self.gyroPort, self.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
        
        # resets all the sensors and motors
        self.reset_all()

    # sets default motor speed
    def setDefaultMotorSpeed(self, speed):
        self.motorSpeed = speed
        return

    # sets the default proportional gain for driving
    def setDriveProportionalGain(self, gain):
        self.driveProportionalGain = gain
        return

    # sets the default proportional gain for turning
    def setTurnProportionalGain(self, gain):
        self.turnProportionalGain = gain
        return
    
    # sets the threshold for the IR sensor when a hazard is present
    def setIrHazardThreshold(self, threshold):
        self.irHazardThreshold = threshold
        return
    
    # sets the threshold for the magnet sensor when a hazard is present
    def setMagnetHazardThreshold(self, threshold):
        self.magnetHazardThreshold = threshold
        return
    
    # sets the encoder distance for 1 unit
    def setEncoderDistance(self, distance):
        self.encoderDistance = distance
        return
    
    # sets the default distance for wall alignment
    def setWallDistance(self, distance):
        self.wallDistance = distance
        return
    
    # sets the default threshold for the wall detection
    def setWallDetectThreshold(self, threshold):
        self.wallDetectThreshold = threshold
        return
    
    # sets the motor speeds
    def setMotorSpeeds(self, rightMotorSpeed, leftMotorSpeed):
        self.set_motor_dps(self.rightMotorPort, rightMotorSpeed)
        self.set_motor_dps(self.leftMotorPort, leftMotorSpeed)
        return
    
    def setMazeValue(self, x, y, value):
        y = len(self.maze)-y-1
        self.maze[y][x] = value
        return
    
    # gets the distances measured by each ultrasonic sensor
    def getDistances(self):
        frontAlignDistance = self.ultrasonicRead(self.frontAlignDistanceSensorPort)
        rearAlignDistance = self.ultrasonicRead(self.rearAlignDistanceSensorPort)
        frontDistanceSensor = self.ultrasonicRead(self.frontDistanceSensorPort)
        return [frontAlignDistance , rearAlignDistance, frontDistanceSensor]
    
    # returns whether a IR hazard is detected
    def getIrHazard(self):
        return (self.analogRead(self.irPort)>=self.irHazardThreshold)

    # returns whether a magnet hazard is detected
    def getMagnetHazard(self):
        mag = 0
        while (mag==0): mag = self.readMagnet()["z"]
        return (mag >= self.magnetHazardThreshold)
    
    # returns the orientation of the robot
    def getOrientation(self):
        return self.orientation
    
    # returns the coordinates of the robot
    def getCoords(self):
        return self.coords
    
    # returns the start coordinates of the robot
    def getStartCoords(self):
        return self.startCoords
    
    def getMaze(self, teamNumber, mapNumber, unitLength, unit, notes=""):
        self.map = self.Map(teamNumber, mapNumber, unitLength, unit, self.startCoords, self.maze, notes)
        return self.map
    
    def stopMotors(self):
        self.set_motor_power(self.rightMotorPort+self.leftMotorPort, 0)
        return

    # moves the robot forward by a certain distance
    def moveUnitForward(self, wallAlign=True):
        # reset motor encoders
        self.offset_motor_encoder(self.rightMotorPort,
                                  self.get_motor_encoder(self.rightMotorPort))
        self.offset_motor_encoder(self.leftMotorPort,
                                  self.get_motor_encoder(self.leftMotorPort))
        # calculate the average reading on an encoder (should be 0 for this one)
        averageEncoderReading = (self.get_motor_encoder(self.rightMotorPort)+
                                 self.get_motor_encoder(self.leftMotorPort))/2

        # while the average encoder reading is less than the distance
        while (averageEncoderReading<self.encoderDistance):
            try:
                # if wall align is true, keep the robot aligned with the wall
                if wallAlign:
                    # get the distances from the ultrasonic sensors
                    distances = self.getDistances()
                    
                    # calculate the error for the wall alignment
                    wallError = (distances[0]-
                                self.setWallDistance)*self.wallAlignProportionalGain
                   
                    # calculate the error for the tilt alignment
                    tiltError = (distances[0]-
                                distances[1])*self.wallAlignProportionalGain

                    # set the motor speeds
                    self.setMotorSpeeds(self.motorSpeed+tiltError+wallError,
                                        self.motorSpeed-tiltError-wallError)
                else:
                    # otherwise, just drive forward for a distance
                    self.setMotorSpeeds(self.motorSpeed, self.motorSpeed)
                
                # calculate the average encoder reading
                averageEncoderReading = (self.get_motor_encoder(self.rightMotorPort)+
                                         self.get_motor_encoder(self.leftMotorPort))/2
            # stop the robot if a keyboard interrupt is detected
            except KeyboardInterrupt:
                self.stopMotors()
                sleep(0.1)
                self.reset_all()
                break
        
        self.stopMotors()
        return
    
    def turn(self, degrees):
        # reset motor encoders
        self.offset_motor_encoder(self.rightMotorPort,
                                  self.get_motor_encoder(self.rightMotorPort))
        self.offset_motor_encoder(self.leftMotorPort,
                                  self.get_motor_encoder(self.leftMotorPort))
        # calibrate gyro sensor
        gyroValue = None
        while gyroValue is None:
            try: gyroValue = self.get_sensor(self.gyroPort)[0]
            except SensorError: continue
        
        sleep(1)
        # turn right
        if (gyroValue < degrees):
            # while the gyro value is less than the degrees
            while (gyroValue < degrees):
                try:
                    # get the gyro value
                    gyroValue = self.get_sensor(self.gyroPort)[0]
                    
                    # calculate the error
                    error = degrees - gyroValue
                    
                    # calculate the motor speeds
                    rightTurnSpeed = -1*error*self.turnProportionalGain
                    leftTurnSpeed = error*self.turnProportionalGain
                    
                    # set the motor speeds
                    self.setMotorSpeeds(rightTurnSpeed, leftTurnSpeed)
                    sleep(0.1)
                
                # stop the robot if a keyboard interrupt is detected
                except KeyboardInterrupt:
                    self.stopMotors()
                    sleep(0.1)
                    self.reset_all()
                    break
        # turn left
        else:
            # while the gyro value is greater than the degrees
            while (gyroValue < degrees):
                try:
                    # get the gyro value
                    gyroValue = self.get_sensor(self.gyroPort)[0]
                    
                    # calculate the error
                    error = degrees - gyroValue

                    # calculate the motor speeds
                    rightTurnSpeed = -1*error*self.turnProportionalGain
                    leftTurnSpeed = error*self.turnProportionalGain
                    
                    # set the motor speeds
                    self.setMotorSpeeds(rightTurnSpeed, leftTurnSpeed)
                    sleep(0.1)
                
                # stop the robot if a keyboard interrupt is detected
                except KeyboardInterrupt:
                    self.stopMotors()
                    sleep(0.1)
                    self.reset_all()
                    break

        self.stopMotors()
        return
    
    def getFrontWall(self):
        return (self.getDistances()[2]<=self.wallDetectThreshold)
    
    def getLeftWall(self):
        return (self.getDistances()[0]<=self.wallDetectThreshold)
    
    # moves the robot "north"
    def moveNorth(self):
        # check the orientation and turn/move accordingly
        if (self.orientation==0): self.moveUnitForward()
        elif (self.orientation==1):
            self.turn(-90)
            self.moveUnitForward()
            self.orientation = 0
        elif (self.orientation==2):
            self.turn(180)
            self.moveUnitForward()
            self.orientation = 0
        else:
            self.turn(90)
            self.moveUnitForward()
            self.orientation = 0
        self.coords[1] += 1
        if (self.getIrHazard()): self.setMazeValue(self.coords[0], self.coords[1], 2)
        elif (self.getMagnetHazard()): self.setMazeValue(self.coords[0], self.coords[1], 3)
        elif (not (self.getFrontWall() or self.getLeftWall())):
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitMaze = True
        else: self.setMazeValue(self.coords[0], self.coords[1], 1)
        return
    
    # same thing for the east
    def moveEast(self):
        if (self.orientation==0):
            self.turn(90)
            self.moveUnitForward()
            self.orientation = 1
        elif (self.orientation==1): self.moveUnitForward()
        elif (self.orientation==2):
            self.turn(-90)
            self.moveUnitForward()
            self.orientation = 1
        else:
            self.turn(180)
            self.moveUnitForward()
            self.orientation = 1
        self.coords[0] += 1
        if (self.getIrHazard()): self.setMazeValue(self.coords[0], self.coords[1], 2)
        elif (self.getMagnetHazard()): self.setMazeValue(self.coords[0], self.coords[1], 3)
        elif (not (self.getFrontWall() or self.getLeftWall())):
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitMaze = True
        else: self.setMazeValue(self.coords[0], self.coords[1], 1)
        return
    
    # and the south
    def moveSouth(self):
        if (self.orientation==0):
            self.turn(180)
            self.moveUnitForward()
            self.orientation = 2
        elif (self.orientation==1):
            self.turn(90)
            self.moveUnitForward()
            self.orientation = 2
        elif (self.orientation==2): self.moveUnitForward()
        else:
            self.turn(-90)
            self.moveUnitForward()
            self.orientation = 2
        self.coords[1] -= 1
        if (self.getIrHazard()): self.setMazeValue(self.coords[0], self.coords[1], 2)
        elif (self.getMagnetHazard()): self.setMazeValue(self.coords[0], self.coords[1], 3)
        elif (not (self.getFrontWall() or self.getLeftWall())):
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitMaze = True
        else: self.setMazeValue(self.coords[0], self.coords[1], 1)
        return
    
    # and the west
    def moveWest(self):
        if (self.orientation==0):
            self.turn(-90)
            self.moveUnitForward()
            self.orientation = 3
        elif (self.orientation==1):
            self.turn(180)
            self.moveUnitForward()
            self.orientation = 3
        elif (self.orientation==2):
            self.turn(90)
            self.moveUnitForward()
            self.orientation = 3
        else: self.moveUnitForward()
        self.coords[0] -= 1
        if (self.getIrHazard()): self.setMazeValue(self.coords[0], self.coords[1], 2)
        elif (self.getMagnetHazard()): self.setMazeValue(self.coords[0], self.coords[1], 3)
        elif (not (self.getFrontWall() or self.getLeftWall())):
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitMaze = True
        else: self.setMazeValue(self.coords[0], self.coords[1], 1)
        return