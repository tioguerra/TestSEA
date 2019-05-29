from testsea import *
import sys
# Path to PyDynamixel
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

CENTER1 = 9.49073913464846
CENTER2 = 9.89417608186238

motor1.sendGoalAngle(CENTER1)
motor2.sendGoalAngle(CENTER2)

port.attachJoints([motor1, motor2])

# Instantiate TestSea object
ts = TestSEA()
while not ts.is_done:
    ts.step()
    val1, val2 = ts.getMotorValues()

    motor1.setGoalAngle(CENTER1+val1)
    motor2.setGoalAngle(CENTER2+val2)

    port.sendGoalAngles()
