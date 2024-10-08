#import necessary libraries
import grovepi as gp
import brickpi3
from MPU9250 import MPU9250
from time import sleep
import numpy as np

# configure brickpi
bp = brickpi3.BrickPi3()
bp.reset_all()

IR_HAZARD = 25
MAG_HAZARD = 50

ULTRASONIC_PORT = 4
IR_PORT = 2

# configure grovepi
gp.set_bus("RPI_1")

# configure MPU9250
mpu = MPU9250()

def getIMUData(offset):
    mag = 0
    while (mag==0):
        magnet = mpu.readMagnet()
        mag = np.linalg.norm([magnet["x"], magnet["y"], magnet["z"]])
    return (mag-offset)

def getIRData():
    return gp.analogRead(2)

def main():
    magOffset = 0
    while (magOffset==0):
        magnet = mpu.readMagnet()
        magOffset = np.linalg.norm([magnet["x"], magnet["y"], magnet["z"]])
    print(magOffset)
    while True:
        try:
            print(f"Front ultrasonic sensor data: {gp.ultrasonicRead(ULTRASONIC_PORT)}")
            print(f"IR sensor data: {gp.analogRead(14)}")
            print(f"IR sensor data: {gp.analogRead(15)}")
            print(f"Magnet sensor data: {getIMUData(magOffset)}\n")
            sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()