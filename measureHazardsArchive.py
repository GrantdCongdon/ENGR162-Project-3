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

def getIMUData():
    mag = 0
    while (mag==0): mag = mpu.readMagnet()["z"]
    return abs(mag)

def getIRData():
    return gp.analogRead(2)

def main():
    while True:
        try:
            print(f"Front ultrasonic sensor data: {gp.ultrasonicRead(ULTRASONIC_PORT)}")
            print(f"IR sensor data: {gp.analogRead(IR_PORT)}")
            print(f"Magnet sensor data: {getIMUData()}\n")
            sleep(1)
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()