#import necessary libraries
import grovepi as gp
import brickpi3
from MPU9250 import MPU9250
from time import sleep

# configure brickpi
bp = brickpi3.BrickPi3()
bp.reset_all()

# paramter constants for the program
rightMotor = bp.PORT_D
leftMotor = bp.PORT_A

motorSpeed = -200

# motor speed
rightMotorSpeed = 0
leftMotorSpeed = 0

# distance sensors
distanceSensor1 = 8
distanceSensor2 = 6
distanceSensor3 = 4

# configure MPU9250
mpu = MPU9250()

# drives the robot forward
def driveForward(motorSpeed):
	bp.set_motor_dps(rightMotor+leftMotor, motorSpeed)

# turns the robot
def turnRobot(rightMotorSpeed, leftMotorSpeed):
	bp.set_motor_dps(rightMotor, rightMotorSpeed)
	bp.set_motor_dps(leftMotor, leftMotorSpeed)

# turns off power to the motors
def stopMotors():
	bp.set_motor_power(rightMotor+leftMotor, 0)

# get turn differential
def getTurnDifferential():
	dist1 = gp.ultrasonicRead(distanceSensor1)
	dist2 = gp.ultrasonicRead(distanceSensor2)
	dist3 = gp.ultrasonicRead(distanceSensor3)
	return [dist1, dist2, dist3]

def moveUnitForward():
	bp.reset_all()
	# reset motor encoders
	bp.offset_motor_encoder(rightMotor, bp.get_motor_encoder(rightMotor))
	bp.offset_motor_encoder(leftMotor, bp.get_motor_encoder(leftMotor))
	while (bp.get_motor_encoder(bp.PORT_A)+bp.get_motor_encoder(bp.PORT_D)< 2112):
		driveForward(motorSpeed)
	stopMotors()

def moveUnitForward2(gain):
	bp.reset_all()
	gyro = bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
	# get reading from brickpi gyro sensor
	degrees = None
	while degrees is None:
		try:
			degrees = bp.get_sensor(bp.PORT_3)[0]
		except brickpi3.SensorError:
			continue
	# reset motor encoders
	bp.offset_motor_encoder(rightMotor, bp.get_motor_encoder(rightMotor))
	bp.offset_motor_encoder(leftMotor, bp.get_motor_encoder(leftMotor))
	totalEncoder = abs(bp.get_motor_encoder(bp.PORT_A)+bp.get_motor_encoder(bp.PORT_D))
	iControl = 0
	while (totalEncoder < 2112):
		try:
			totalEncoder = abs(bp.get_motor_encoder(bp.PORT_A)+bp.get_motor_encoder(bp.PORT_D))
			motorSpeed = (totalEncoder - 2112)*gain
			iControl += (totalEncoder - 2112)*0.00001
			driveForward(motorSpeed+iControl)
		except KeyboardInterrupt:
			stopMotors()
			sleep(0.1)
			bp.reset_all()
			break
	
	stopMotors()
	# get reading from brickpi gyro sensor
	gyroValue = None

	while gyroValue is None:
		try:
			gyroValue = bp.get_sensor(bp.PORT_3)[0]
		except brickpi3.SensorError:
			continue
	
	while (gyroValue != degrees):
		try:
			gyroValue = bp.get_sensor(bp.PORT_3)[0]
			error = 0 - gyroValue
			rightTurnSpeed = -1*error*6
			leftTurnSpeed = error*6
			turnRobot(rightTurnSpeed, leftTurnSpeed)
		except brickpi3.SensorError:
			continue
	
	stopMotors()
	sleep(0.1)

def turn(degrees, gain):
	bp.reset_all()
	gyro = bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
	# get reading from brickpi gyro sensor
	gyroValue = None
	while gyroValue is None:
		try:
			gyroValue = bp.get_sensor(bp.PORT_3)[0]
		except brickpi3.SensorError:
			continue
	while (gyroValue != degrees):
		try:
			gyroValue = bp.get_sensor(bp.PORT_3)[0]
			print(gyroValue)
			error = degrees - gyroValue
			rightTurnSpeed = -1*error*gain
			leftTurnSpeed = error*gain
			
			turnRobot(rightTurnSpeed, leftTurnSpeed)
			sleep(0.1)
		except KeyboardInterrupt:
			stopMotors()
			sleep(0.1)
			bp.reset_all()
			break

	stopMotors()
	sleep(0.1)
def getIrHazard():
	return (gp.analogRead(2) >= 25)
def getMagnetHazard():
	mag = 0
	while (mag==0): mag = mpu.readMagnet()["z"]
	return (mag >= 50)

def goToPoint(startCoords, endCoords, orientation):
	currentPosition = [startCoords[0], startCoords[1]]
	while currentPosition != endCoords:
		try:
			if (currentPosition[0]<endCoords[0]):
				if (orientation != 1):
					turn(90*(1-orientation), 4)
					orientation = 1
				if (not getIrHazard() and not getMagnetHazard()):
					moveUnitForward2(0.2)
					currentPosition[0] += 1
				else:
					turn(-90, 4)
					orientation -= 1 if orientation > 0 else -3
					moveUnitForward2(0.2)
					currentPosition[1] += 1
			elif (currentPosition[1]<endCoords[1]):
				if (orientation != 0):
					turn(-90*(orientation), 4)
					orientation = 0
				if (not getIrHazard() and not getMagnetHazard()):
					moveUnitForward2(0.2)
					currentPosition[1] += 1
				else:
					turn(-90, 4)
					orientation -= 1 if orientation > 0 else -3
					moveUnitForward2(0.2)
					currentPosition[0] += 1
			elif (currentPosition[0]>endCoords[0]):
				if (orientation != 3):
					turn(90*(3-orientation), 4)
					orientation = 3
				if (not getIrHazard() and not getMagnetHazard()):
					moveUnitForward2(0.2)
					currentPosition[0] -= 1
				else:
					turn(90, 4)
					orientation += 1 if orientation < 3 else -3
					moveUnitForward2(0.2)
					currentPosition[1] += 1
			elif (currentPosition[1]>endCoords[1]):
				if (orientation != 2):
					turn(90*(2-orientation), 4)
					orientation = 2
				if (not getIrHazard() and not getMagnetHazard()):
					moveUnitForward2(0.2)
					currentPosition[1] -= 1
				else:
					turn(90, 4)
					orientation += 1 if orientation < 3 else -3
					moveUnitForward2(0.2)
					currentPosition[0] += 1
		except KeyboardInterrupt:
			stopMotors()
			sleep(0.1)
			bp.reset_all()
			break
		sleep(1)
	
	return [currentPosition, orientation]

if __name__ == "__main__":
	startingPosition = input("Enter starting position in coordinate form: ")[1:-1].split(",")
	startingPosition = [int(coord) for coord in startingPosition]

	endPosition1 = input("Enter end position 1 in coordinate form: ")[1:-1].split(",")
	endPosition1 = [int(coord) for coord in endPosition1]

	endPosition2 = input("Enter end position 2 in coordinate form: ")[1:-1].split(",")
	endPosition2 = [int(coord) for coord in endPosition2]

	endPosition3 = input("Enter end position 3 in coordinate form: ")[1:-1].split(",")
	endPosition3 = [int(coord) for coord in endPosition3]

	endPosition4 = input("Enter end position 4 in coordinate form: ")[1:-1].split(",")
	endPosition4 = [int(coord) for coord in endPosition4]

	orientation = int(input("Enter orientation: "))

	endValues = goToPoint(startingPosition, endPosition1, orientation)
	input()

	endValues = goToPoint(endValues[0], endPosition2, endValues[1])
	input()

	endValues = goToPoint(endValues[0], endPosition3, endValues[1])
	input()

	endValues = goToPoint(endValues[0], endPosition4, endValues[1])
	input()