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

def followWall(dist, gain):
	# dist[0] is the rear sensor and dist[1] is the upper sensor
	while True:
		try:
			dists = getTurnDifferential()
			print(f"Rear sensor: {dists[0]}\t\tUpper sensor: {dists[1]}\tFront sensor: {dists[2]}")
			wallError = (dists[1] - dist)*gain
			tiltError = (dists[1] - dists[0])*gain
			turnRobot(motorSpeed+tiltError+wallError, motorSpeed-tiltError-wallError)
			"""if (dists[1]<=10):
				turnRobot(0, -100)
			elif dists[0]<dists[1]-1:
				turnRobot(-100, 0)
				print("Turning right")
			elif dists[1]<dists[0]-1:
				turnRobot(0, -100)
				print("Turning left")
			else:
				driveForward(motorSpeed)
				print("Going straight")"""
			
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

def turn(degrees, gain):
	bp.reset_all()
	gyro = bp.set_sensor_type(bp.PORT_3, bp.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
	# get reading from brickpi gyro sensor
	gyroValue = None
	while gyroValue is None:
		try:
			gyroValue = bp.get_sensor(bp.PORT_3)[0]
		except brickpi3.SensorError:
			print("Calibrating Gyro")
			continue
	print(gyroValue)
	sleep(5)
	if (gyroValue < degrees):
		rightTurnSpeed = 100
		leftTurnSpeed = -100
		while (gyroValue < degrees):
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
	else:
		rightTurnSpeed = -100
		leftTurnSpeed = 100
		while (gyroValue < degrees):
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

if __name__ == "__main__":
	# gain of 10 works well
	dist = int(input("Distance from wall: "))
	gain = int(input("Gain: "))
	followWall(dist, gain)