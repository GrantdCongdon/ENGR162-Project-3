#import necessary libraries
import grovepi as gp
import brickpi3
from MPU9250 import MPU9250
from time import sleep

# configure brickpi
bp = brickpi3.BrickPi3()


# paramter constants for the program
rightMotor = bp.PORT_A
leftMotor = bp.PORT_D

motorSpeed = -100

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
def followWall():
	# dist[0] is the rear sensor and dist[1] is the front sensor
	while True:
		try:
			dists = getTurnDifferential()
			print(f"Rear sensor: {dists[0]}\t Upper sensor: {dists[1]}\tFront sensor: {dists[2]}")
			if (dists[1]<=3):
				turnRobot(0, -100)
			elif dists[0]<dists[1]-1:
				turnRobot(-100, 0)
				print("Turning right")
			elif dists[1]<dists[0]-1:
				turnRobot(0, -100)
				print("Turning left")
			else:
				driveForward(motorSpeed)
				print("Going straight")
			if (dists[2]< 15):
				if (dists[1]<15):
					turnRobot(0, -150)
					sleep(5)
				else:
					turnRobot(-150, 0)
					sleep(5)

		except KeyboardInterrupt:
			stopMotors()
			sleep(0.1)
			bp.reset_all()
			break

if __name__ == "__main__":
    followWall()