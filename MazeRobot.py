#import necessary libraries
import grovepi as gp
from brickpi3 import BrickPi3, SensorError
from MPU9250 import MPU9250
from time import sleep, time
from math import pi

# class that covers all the aspects of the ENGR161/162 robot
class MazeRobot(BrickPi3):
    # define IMU
    imu = MPU9250()
    
    class Hazard(Exception):
        def __init__(self, message=""):
            self.message = "Detected " + message +" Hazard!"
            super().__init__(self.message)

        def __str__(self):
            return self.message
        
        def __repr__(self):
            return self.__str__()
    
    # class that defines the map of the maze
    class Map:
        def __init__(self, teamNumber: int, mapNumber:int , unitLength: int, unit: str, origin: list, map: list, hazards: list, notes=""):
            # initializes the map with the team number, map number, unit length, unit, notes, origin, and map
            self.teamNumber = teamNumber
            self.mapNumber = mapNumber
            self.unitLength = unitLength
            self.unit = unit
            self.notes = notes
            self.origin = origin
            self.map = map
            self.hazards = hazards

        # overrides the string method to print out the map
        def __str__(self):
            basicInfo = f"Team Number: {self.teamNumber}\nMap Number: {self.mapNumber}\nUnit Length: {self.unitLength}\nUnit: {self.unit}\nOrigin: {self.origin}\nNotes: {self.notes}\n"
            mapInfo = ""
            for row in self.map:
                for cell in row:
                    if (cell<0): cell = 1
                    mapInfo += f"{cell}, "
                mapInfo += "\n"
            return basicInfo + mapInfo
        
        def __repr__(self):
            return self.__str__()
        
        # function that converts the map into a string then writes it to a file
        def toCSV(self, fileName: str):
            csvString = ""

            # loop through each line of the export string and add a comma if necessary
            for line in str(self).split("\n"):
                if (line!="" and line[-1]!=","): csvString += line + ",\n"
                else: csvString += line + "\n"

            # write the string to a file
            with open(fileName+".csv", "w") as file:
                file.write(csvString)
            return
        
        # function that converts the hazards into a string then writes it to a file
        def hazardsToCSV(self, fileName: str):
            csvString = "Hazard Type, Parameter of Interest, Parameter Value, Hazard X-Coordinate, Hazard Y-Coordinate\n"
            for hazard in self.hazards:
                csvString += f"{hazard['Hazard Type']}, {hazard['Parameter of Interest']}, {hazard['Parameter Value']}, {hazard['Hazard X-Coordinate']}, {hazard['Hazard Y-Coordinate']}\n"
            with open(fileName+".csv", "w") as file:
                file.write(csvString)
            return
    
    # define wheel diameter of the robot
    wheelDiameter = 4.2

    # define distance of 1 unit
    unitDistance = 40

    # defines the default motor speed to go forward at
    motorSpeed = -200

    # defines center motor speed
    centerMotorSpeed = -100

    # define default cargo motor speed
    cargoMotorSpeed = -90
    
    # defines the default proportional gain for driving and turning
    turnProportionalGain = 4
    wallAlignProportionalGain = 10
    
    # defines the default threshold for the IR sensor when a hazard is present
    irHazardThreshold = 25
    
    # defines the default threshold for the magnet sensor when hazard is present
    magnetHazardThreshold = 100

    # encoder distance for 1 unit
    encoderDistance = (360/(pi*wheelDiameter)) * unitDistance

    # encoder distance to deploy cargo
    cargoEncoderDistance = 200

    # default distance for wall alignment
    wallDistance=10

    # default center distance
    centerDistance = 15

    # default threshold for the wall detection
    wallDetectThreshold = 20

    # define 90 degree turn
    squareTurn = 90

    # define half rotation
    aboutFace = 180

    # define whether in the maze or not
    exitedMaze = False

    # intakes the default ports for the motors, ultrasonics, gyro, and IR sensor
    def __init__(self, rightMotorPort: int, leftMotorPort: int, cargoPort: int, frontAlignDistanceSensorPort: int, rearAlignDistanceSensorPort: int,
                 frontDistanceSensorPort: int, rightDistancePort: int, gyroPort: int, irPort: int, touchPort: int, coords: tuple, mazeSize: tuple,
                 orientation=0):

        # initializes the brickpi3, MPU9250, and grovepi
        super().__init__()
        
        # takes parameters and assigns them to the class
        self.rightMotorPort = rightMotorPort
        self.leftMotorPort = leftMotorPort
        self.cargoPort = cargoPort
        self.frontAlignDistanceSensorPort = frontAlignDistanceSensorPort
        self.rearAlignDistanceSensorPort = rearAlignDistanceSensorPort
        self.frontDistanceSensorPort = frontDistanceSensorPort
        self.rightDistancePort = rightDistancePort
        self.gyroPort = gyroPort
        self.irPort = irPort
        self.touchPort = touchPort
        self.coords = list(coords)
        self.orientation = orientation
        self.startCoords = coords
        self.maze = [[0 for _ in range(mazeSize[0])] for _ in range(mazeSize[1])]
        self.hazards = []
        self.setMazeValue(coords[0], coords[1], 5)

        # configure grovepi
        gp.set_bus("RPI_1")
        
        self.set_sensor_type(self.rightDistancePort, self.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        self.set_sensor_type(self.gyroPort, self.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

        # configure gyro sensor
        self.resetAll()

    # sets wheel diameter
    def setWheelDiameter(self, diameter: float):
        self.wheelDiameter = diameter
        self.encoderDistance = (360/(pi*self.wheelDiameter)) * self.unitDistance
        return

    # sets default motor speed
    def setDefaultMotorSpeed(self, speed: int):
        self.motorSpeed = speed
        return
    
    # sets the default center motor speed
    def setCenterMotorSpeed(self, speed: int):
        self.centerMotorSpeed = speed
        return

    # sets the default proportional gain for turning
    def setTurnProportionalGain(self, gain: float):
        self.turnProportionalGain = gain
        return
    
    # sets the threshold for the IR sensor when a hazard is present
    def setIrHazardThreshold(self, threshold: int):
        self.irHazardThreshold = threshold
        return
    
    # sets the threshold for the magnet sensor when a hazard is present
    def setMagnetHazardThreshold(self, threshold: int):
        self.magnetHazardThreshold = threshold
        return
    
    # sets the size of one unit
    def setUnitDistance(self, distance: float):
        self.unitDistance = distance
        self.encoderDistance = (360/(pi*self.wheelDiameter)) * self.unitDistance
        return
    
    # sets the default distance for wall alignment
    def setWallDistance(self, distance: int):
        self.wallDistance = distance
        return
    
    # sets the default center distance
    def setCenterDistance(self, distance: int):
        self.centerDistance = distance
        return
    
    # sets the default threshold for the wall detection
    def setWallDetectThreshold(self, threshold: int):
        self.wallDetectThreshold = threshold
        return
    
    # sets the motor speeds
    def setMotorSpeeds(self, rightMotorSpeed: int, leftMotorSpeed: int):
        self.set_motor_dps(self.rightMotorPort, rightMotorSpeed)
        self.set_motor_dps(self.leftMotorPort, leftMotorSpeed)
        return
    
    # set a value for a maze cell
    def setMazeValue(self, x: int, y: int, value: int):
        y = len(self.maze)-y-1
        self.maze[y][x] = value
        return
    
    # set the wheel diameter
    def setWheelDiameter(self, diameter: float):
        self.wheelDiameter = diameter
        # encoder distance for 1 unit
        self.encoderDistance = (360/(2*pi*self.wheelDiameter)) * self.unitDistance
        return
    
    # returns the orientation of the robot
    @property
    def heading(self):
        return self.orientation
    
    # returns the coordinates of the robot
    @property
    def location(self):
        return self.coords
    
    # returns the start coordinates of the robot
    @property
    def startLocation(self):
        return self.startCoords

    # gets the distances measured by each ultrasonic sensor
    def getDistances(self):
        frontAlignDistance = gp.ultrasonicRead(self.frontAlignDistanceSensorPort)
        while (frontAlignDistance >= 498): frontAlignDistance = gp.ultrasonicRead(self.frontAlignDistanceSensorPort)
        rearAlignDistance = gp.ultrasonicRead(self.rearAlignDistanceSensorPort)
        while (rearAlignDistance >= 498): rearAlignDistance = gp.ultrasonicRead(self.rearAlignDistanceSensorPort)
        frontDistance = gp.ultrasonicRead(self.frontDistanceSensorPort)
        while (frontDistance >= 498): frontDistance = gp.ultrasonicRead(self.frontDistanceSensorPort)
        rightDistance = None
        while rightDistance is None:
            try: rightDistance = self.get_sensor(self.rightDistancePort)
            except OSError: self.set_sensor_type(self.rightDistancePort, self.SENSOR_TYPE.EV3_ULTRASONIC_CM)
            except (SensorError): continue
        return [frontAlignDistance , rearAlignDistance, frontDistance, rightDistance]
    
    # returns whether a IR hazard is detected
    def getIrHazard(self):
        return (gp.analogRead(self.irPort)>=self.irHazardThreshold)

    # returns whether a magnet hazard is detected
    def getMagnetHazard(self):
        mag = 0
        while (mag==0): mag = self.imu.readMagnet()["z"]
        return (mag >= self.magnetHazardThreshold)
    
    def getMap(self, teamNumber: int, mapNumber: int, unitLength:int , unit: str, notes="None"):
        self.map = self.Map(teamNumber, mapNumber, unitLength, unit, self.startCoords, self.maze, self.hazards, notes)
        return self.map
    
    def getFrontWall(self):
        return (self.getDistances()[2] <= self.wallDetectThreshold)
    
    def getLeftWall(self):
        return (self.getDistances()[0] <= self.wallDetectThreshold)
    
    def getRightWall(self):
        return (self.getDistances()[3] <= self.wallDetectThreshold)
    
    def getNorthWall(self):
        if (self.orientation==0): return self.getFrontWall()
        elif (self.orientation==1): return self.getLeftWall()
        elif (self.orientation==2): return False
        else: return self.getRightWall()

    def getEastWall(self):
        if (self.orientation==0): return self.getRightWall()
        elif (self.orientation==1): return self.getFrontWall()
        elif (self.orientation==2): return self.getLeftWall()
        else: return False

    def getSouthWall(self):
        if (self.orientation==0): return False
        elif (self.orientation==1): return self.getRightWall()
        elif (self.orientation==2): return self.getFrontWall()
        else: return self.getLeftWall()

    def getWestWall(self):
        if (self.orientation==0): return self.getLeftWall()
        elif (self.orientation==1): return False
        elif (self.orientation==2): return self.getRightWall()
        else: return self.getFrontWall()

    # set a value for a maze cell
    def getMazeValue(self, x: int, y: int):
        y = len(self.maze)-y-1
        try: return self.maze[y][x]
        except IndexError: -5
    
    def resetAll(self):
        # reset motor encoders
        self.offset_motor_encoder(self.rightMotorPort,
                                  self.get_motor_encoder(self.rightMotorPort))
        self.offset_motor_encoder(self.leftMotorPort,
                                  self.get_motor_encoder(self.leftMotorPort))

        gyroValue = None
        while gyroValue is None:
            try: gyroValue = self.get_sensor(self.gyroPort)[0]
            except OSError: self.set_sensor_type(self.gyroPort, self.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
            except (SensorError): continue
        
        while gyroValue != 0:
            self.reset_all()
            # calibrate gyro sensor
            gyroValue = None
            while gyroValue is None:
                try: gyroValue = self.get_sensor(self.gyroPort)[0]
                except OSError: self.set_sensor_type(self.gyroPort, self.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
                except (SensorError): continue

        # reinitialize the sensors
        self.set_sensor_type(self.rightDistancePort, self.SENSOR_TYPE.EV3_ULTRASONIC_CM)
        return
    
    def stopMotors(self):
        self.set_motor_dps(self.rightMotorPort+self.leftMotorPort, 0)
        sleep(0.1)
        self.set_motor_power(self.rightMotorPort+self.leftMotorPort, 0)
        return

    # moves the robot forward by a certain distance
    def moveUnitForward(self, wallAlign=True):
        self.resetAll()
        # calculate the average reading on an encoder (should be 0 for this one)
        averageEncoderReading = abs((self.get_motor_encoder(self.rightMotorPort)+
                                 self.get_motor_encoder(self.leftMotorPort))/2)

        # while the average encoder reading is less than the distance
        while (averageEncoderReading<self.encoderDistance):
            # get the distances from the ultrasonic sensors
            distances = self.getDistances()
            if (distances[0] > self.wallDetectThreshold or distances[1] > self.wallDetectThreshold): wallPresent = False
            else: wallPresent = True
            try:
                
                # if wall align is true, keep the robot aligned with the wall
                if wallAlign and wallPresent:

                    if (distances[2] <= self.centerDistance): break
                    
                    # calculate the error for the wall alignment
                    wallError = (distances[0]-
                                self.wallDistance)*self.wallAlignProportionalGain
                   
                    # calculate the error for the tilt alignment
                    tiltError = (distances[0]-
                                distances[1])*self.wallAlignProportionalGain

                    # set the motor speeds
                    self.setMotorSpeeds(self.motorSpeed+tiltError+wallError,
                                        self.motorSpeed-tiltError-wallError)
                else:
                    # otherwise, just drive forward for a distance
                    self.setMotorSpeeds(self.motorSpeed, self.motorSpeed)

                    # make sure we don't run into the front wall
                    if (distances[2] <= self.centerDistance): break
                
                # calculate the average encoder reading
                averageEncoderReading = abs((self.get_motor_encoder(self.rightMotorPort)+
                                         self.get_motor_encoder(self.leftMotorPort))/2)
            # stop the robot if a keyboard interrupt is detected
            except KeyboardInterrupt:
                self.stopMotors()
                sleep(0.1)
                self.reset_all()
                break
        
        self.stopMotors()
        return
    
    def turn(self, degrees):
        # reset the motors and sensors
        self.resetAll()
        
        # get the gyro value
        gyroValue = self.get_sensor(self.gyroPort)[0]
        
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
                    
                    if (abs(rightTurnSpeed) < 5): rightTurnSpeed = -5
                    if (abs(leftTurnSpeed) < 5): leftTurnSpeed = 5

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
            while (gyroValue > degrees):
                try:
                    # get the gyro value
                    gyroValue = self.get_sensor(self.gyroPort)[0]
                    
                    # calculate the error
                    error = degrees - gyroValue

                    # calculate the motor speeds
                    rightTurnSpeed = -1*error*self.turnProportionalGain
                    leftTurnSpeed = error*self.turnProportionalGain

                    if (abs(rightTurnSpeed) < 5): rightTurnSpeed = 5
                    if (abs(leftTurnSpeed) < 5): leftTurnSpeed = -5
                    
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
    
    def depositCargo(self):
        # reset cargo encoder
        self.offset_motor_encoder(self.cargoPort, self.get_motor_encoder(self.cargoPort))

        # read the encoder value for the cargo motor
        cargoEncoderReading = abs(self.get_motor_encoder(self.cargoPort))

        while (cargoEncoderReading<self.cargoEncoderDistance):
            try:
                # set the motor speed
                self.set_motor_dps(self.cargoPort, self.cargoMotorSpeed)
                
                # read the encoder value
                cargoEncoderReading = abs(self.get_motor_encoder(self.cargoPort))
            
            except KeyboardInterrupt:
                self.set_motor_power(self.cargoPort, 0)
                sleep(0.1)
                self.reset_all()
                break

        self.set_motor_power(self.cargoPort, 0)
        return
    
    # moves the robot to the center of the cell
    def moveCenter(self):
        # get the front distance
        frontDistance = self.getDistances()[2]
        # move the robot to the center of the cell
        if (frontDistance>self.centerDistance):
            while (frontDistance>self.centerDistance):
                try:
                    self.setMotorSpeeds(self.centerMotorSpeed, self.centerMotorSpeed)
                    frontDistance = self.getDistances()[2]
                except KeyboardInterrupt:
                    self.stopMotors()
                    sleep(0.1)
                    self.reset_all()
                    break
        else:
            while (frontDistance<self.centerDistance):
                try:
                    self.setMotorSpeeds(-1*self.centerMotorSpeed, -1*self.centerMotorSpeed)
                    frontDistance = self.getDistances()[2]
                except KeyboardInterrupt:
                    self.stopMotors()
                    sleep(0.1)
                    self.reset_all()
                    break

        self.stopMotors()
        return
    
    # moves the robot "north"
    def moveNorth(self, wallAlign=True):
        # check for hazards and walls and update the maze
        if (self.getIrHazard()):
            self.setMazeValue(self.coords[0], self.coords[1]+1, 2)
            self.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(self.irPort), "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("IR")
        elif (self.getMagnetHazard()):
            self.setMazeValue(self.coords[0], self.coords[1]+1, 3)
            self.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": self.imu.readMagnet()["z"], "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("Magnet")
        
        # check the orientation and turn/move accordingly
        if (self.orientation==0): self.moveUnitForward(wallAlign)
        elif (self.orientation==1):
            self.turn(-self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 0
        elif (self.orientation==2):
            self.turn(self.aboutFace)
            self.moveUnitForward(wallAlign)
            self.orientation = 0
        else:
            self.turn(self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 0
        
        # update the coordinates
        try: self.coords[1] += 1
        except IndexError:
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitedMaze = True
            return
        
        # sets a maze value of -1 if there is a wall on all sides or if the cell is not a junction
        if ((self.getMazeValue(self.coords[0], self.coords[1])!=5 or self.getMazeValue(self.coords[0], self.coords[1])!=4) and
            ((self.getNorthWall() and self.getEastWall() and self.getWestWall()) or (self.getEastWall() and self.getWestWall() and
                                                                                     self.getMazeValue(self.coords[0], self.coords[1]-1)==-1))):
            self.setMazeValue(self.coords[0], self.coords[1], -1)

        elif (self.getMazeValue(self.coords[0], self.coords[1])==0):
            self.setMazeValue(self.coords[0], self.coords[1], 1)
        
        # centers the robot in the cell front to back
        if (wallAlign and self.getFrontWall()): self.moveCenter()
        
        return
    
    # same thing for the east
    def moveEast(self, wallAlign=True):
        # check for hazards and walls and update the maze
        if (self.getIrHazard()):
            self.setMazeValue(self.coords[0]+1, self.coords[1], 2)
            self.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(self.irPort), "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("IR")
        elif (self.getMagnetHazard()):
            self.setMazeValue(self.coords[0]+1, self.coords[1], 3)
            self.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": self.imu.readMagnet()["z"], "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("Magnet")
            
        if (self.orientation==0):
            self.turn(self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 1
        elif (self.orientation==1): self.moveUnitForward(wallAlign)
        elif (self.orientation==2):
            self.turn(-self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 1
        else:
            self.turn(self.aboutFace)
            self.moveUnitForward(wallAlign)
            self.orientation = 1
        
        # update the coordinates
        try: self.coords[0] += 1
        except IndexError:
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitedMaze = True
            return
        
        # sets a maze value of -1 if there is a wall on all sides or if the cell is not a junction
        if ((self.getMazeValue(self.coords[0], self.coords[1])!=5 or self.getMazeValue(self.coords[0], self.coords[1])!=4) and
            ((self.getNorthWall() and self.getSouthWall() and self.getEastWall()) or (self.getNorthWall() and self.getSouthWall() and
                                                                                     self.getMazeValue(self.coords[0]-1, self.coords[1])==-1))):
            self.setMazeValue(self.coords[0], self.coords[1], -1)

        elif (self.getMazeValue(self.coords[0], self.coords[1])==0):
            self.setMazeValue(self.coords[0], self.coords[1], 1)

        # centers the robot in the cell front to back
        if (wallAlign and self.getFrontWall()): self.moveCenter()

        return
    
    # and the south
    def moveSouth(self, wallAlign=True):
        # check for hazards and walls and update the maze
        if (self.getIrHazard()):
            self.setMazeValue(self.coords[0], self.coords[1]-1, 2)
            self.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(self.irPort), "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("IR")
        elif (self.getMagnetHazard()):
            self.setMazeValue(self.coords[0], self.coords[1]-1, 3)
            self.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": self.imu.readMagnet()["z"], "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("Magnet")
            
        if (self.orientation==0):
            self.turn(self.aboutFace)
            self.moveUnitForward(wallAlign)
            self.orientation = 2
        elif (self.orientation==1):
            self.turn(self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 2
        elif (self.orientation==2): self.moveUnitForward(wallAlign)
        else:
            self.turn(-self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 2
        
        # update the coordinates
        try: self.coords[1] -= 1
        except IndexError:
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitedMaze = True
            return
        
        if ((self.getMazeValue(self.coords[0], self.coords[1])!=5 or self.getMazeValue(self.coords[0], self.coords[1])!=4) and
            ((self.getEastWall() and self.getWestWall() and self.getSouthWall()) or (self.getEastWall() and self.getWestWall() and
                                                                                        self.getMazeValue(self.coords[0], self.coords[1]+1)==-1))):
            self.setMazeValue(self.coords[0], self.coords[1], -1)
        elif (self.getMazeValue(self.coords[0], self.coords[1])==0):
            self.setMazeValue(self.coords[0], self.coords[1], 1)

        # centers the robot in the cell front to back
        if (wallAlign and self.getFrontWall()): self.moveCenter()

        return
    
    # and the west
    def moveWest(self, wallAlign=True):
        # check for hazards and walls and update the maze
        if (self.getIrHazard()):
            self.setMazeValue(self.coords[0]-1, self.coords[1], 2)
            self.hazards.append({"Hazard Type": "High Temperature Heat Source", "Parameter of Interest": "Radiated Power (W)",
                                 "Parameter Value": gp.analogRead(self.irPort), "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("IR")
        elif (self.getMagnetHazard()):
            self.setMazeValue(self.coords[0]-1, self.coords[1], 3)
            self.hazards.append({"Hazard Type": "Electric/Magnetic Activity Source", "Parameter of Interest": "Field Strength (uT)",
                                 "Parameter Value": self.imu.readMagnet()["z"], "Hazard X-Coordinate": self.coords[0]*self.unitDistance,
                                 "Hazard Y-Coordinate": self.coords[1]*self.unitDistance})
            raise self.Hazard("Magnet")

        if (self.orientation==0):
            self.turn(-self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 3
        elif (self.orientation==1):
            self.turn(self.aboutFace)
            self.moveUnitForward(wallAlign)
            self.orientation = 3
        elif (self.orientation==2):
            self.turn(self.squareTurn)
            self.moveUnitForward(wallAlign)
            self.orientation = 3
        else: self.moveUnitForward(wallAlign)
        
        # update the coordinates
        try: self.coords[0] -= 1
        except IndexError:
            self.setMazeValue(self.coords[0], self.coords[1], 4)
            self.exitedMaze = True
            return
        
        if ((self.getMazeValue(self.coords[0], self.coords[1])!=5 or self.getMazeValue(self.coords[0], self.coords[1])!=4) and
            ((self.getNorthWall() and self.getSouthWall() and self.getWestWall()) or (self.getNorthWall() and self.getSouthWall() and
                                                                                     self.getMazeValue(self.coords[0]+1, self.coords[1])==-1))):
            self.setMazeValue(self.coords[0], self.coords[1], -1)
        elif (self.getMazeValue(self.coords[0], self.coords[1])==0):
            self.setMazeValue(self.coords[0], self.coords[1], 1)

        # centers the robot in the cell front to back
        if (wallAlign and self.getFrontWall()): self.moveCenter()

        return
    
    def celebrate(self):
        startTime = time()
        while (time()-startTime<10):
            self.set_motor_dps(self.rightMotorPort, 360)
            self.set_motor_dps(self.leftMotorPort, -360)
        self.stopMotors()
        sleep(0.1)
        self.reset_all()
        return