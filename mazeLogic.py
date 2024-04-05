#import necessary libraries
import grovepi as gp
import brickpi3
from MPU9250 import MPU9250
from time import sleep
from math import pi

# configure brickpi
bp = brickpi3.BrickPi3()
bp.reset_all()

# configure MPU9250
mpu = MPU9250()

# configure gyro sensor
gyro = bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

# paramter constants for the program
rightMotor = bp.PORT_D
leftMotor = bp.PORT_A
gyroSensor = bp.PORT_3

# distance sensors
frontRightDistanceSensor = 6
backRightDistanceSensor = 8
forwardDistanceSensor = 4

# wheel diameter
wheelDiameter = 5.5

# turns off power to the motors
def stopMotors():
	bp.set_motor_dps(rightMotor+leftMotor, 0)
	sleep(0.1)
	bp.set_motor_power(rightMotor+leftMotor, 0)
	return

# drives the robot forward
def driveForward(motorSpeed):
	bp.set_motor_dps(rightMotor+leftMotor, motorSpeed)
	return

# turns the robot
def turnRobot(rightMotorSpeed, leftMotorSpeed):
	bp.set_motor_dps(rightMotor, rightMotorSpeed)
	bp.set_motor_dps(leftMotor, leftMotorSpeed)
	return

# get turn differential
def getDistances():
	# measure the distance from each sensor
	frontRightDistance = gp.ultrasonicRead(frontRightDistanceSensor)
	frontLeftDistance = gp.ultrasonicRead(backRightDistanceSensor)
	forwardDistance = gp.ultrasonicRead(forwardDistanceSensor)
	# return the distances
	return [frontRightDistance, frontLeftDistance, forwardDistance]

def followWall(distanceFromWall, gain, distanceToTravel, motorSpeed=-200):
	# dist[0] is the rear sensor and dist[1] is the upper sensor
	bp.reset_all()
	
	# get reading from brickpi gyro sensor
	degrees = None
	while degrees is None:
		try: degrees = bp.get_sensor(gyroSensor)[0]
		except brickpi3.SensorError: continue
	
	# reset motor encoders
	bp.offset_motor_encoder(rightMotor, bp.get_motor_encoder(rightMotor))
	bp.offset_motor_encoder(leftMotor, bp.get_motor_encoder(leftMotor))
    
	totalEncoder = abs(bp.get_motor_encoder(bp.PORT_A)+bp.get_motor_encoder(bp.PORT_D))
	
	while ((totalEncoder/360)*wheelDiameter*pi < distanceToTravel):
		try:
			dists = getDistances()
			print(f"Rear sensor: {dists[0]}\t\tUpper sensor: {dists[1]}\tFront sensor: {dists[2]}")
			wallError = (dists[1] - distanceFromWall)*gain
			tiltError = (dists[1] - dists[0])*gain
			turnRobot(motorSpeed+tiltError+wallError, motorSpeed-tiltError-wallError)
			if (dists[2] < 20):
				if (dists[1]<15):
					turn(90, 4)
				else:
					turn(-90, 4)

		except KeyboardInterrupt:
			stopMotors()
			sleep(0.1)
			bp.reset_all()
			break