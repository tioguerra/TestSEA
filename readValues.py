from testsea import *
import sys
sys.path.append("/home/guichristmann/Repos/PyDynamixel/")
from pyjoints import Joint, DxlComm

PORT = "/dev/ttyUSB0"
BAUDRATE = 1

MOTOR1_ID = 1
MOTOR2_ID = 2

# Instantiate port
port = DxlComm(PORT, BAUDRATE)

# Instantiate joint objects for both motors
motor1 = Joint(MOTOR1_ID)
motor2 = Joint(MOTOR2_ID)

port.attachJoints([motor1, motor2])

while True:
    pos1 = motor1.receiveCurrAngle()
    pos2 = motor2.receiveCurrAngle()

    print(pos1, pos2)
