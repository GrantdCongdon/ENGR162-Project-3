import brickpi3
from time import sleep

# configure brickpi
bp = brickpi3.BrickPi3()
bp.reset_all()

# paramter constants for the program
rightMotor = bp.PORT_A
leftMotor = bp.PORT_D

# turns the robot
def turnRobot(rightMotorSpeed, leftMotorSpeed):
	bp.set_motor_dps(rightMotor, rightMotorSpeed)
	bp.set_motor_dps(leftMotor, leftMotorSpeed)

# turns off power to the motors
def stopMotors():
	bp.set_motor_power(rightMotor+leftMotor, 0)
	
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
	if (gyroValue < degrees):
		rightTurnSpeed = 100
		leftTurnSpeed = -100
		while (gyroValue < degrees):
			try:
				gyroValue = bp.get_sensor(bp.PORT_3)[0]
				print(gyroValue)
				error = degrees - gyroValue
				rightTurnSpeed = error*gain
				leftTurnSpeed = -1*error*gain
				
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

def main():
	degrees = float(input("Enter number of degrees to rotate (positive for clockwise): "))
	turn(degrees, 4)

if __name__ == "__main__":
	main()
	
