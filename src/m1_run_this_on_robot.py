"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Nicholas Snow.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import math

class DelegateThatReceives(object):

    def __init__(self,robot):
        self.robot=robot = bot.RoseBot()
    def Forward(self, leftspeed,rightspeed):
        print("Forward",leftspeed,rightspeed)
        self.robot.drive_system.go(leftspeed,rightspeed)
    def Backward(self, leftspeed,rightspeed):
        print("Backward",leftspeed,rightspeed)
        self.robot.drive_system.go(-leftspeed, -rightspeed)
    def Arm_Up(self):
        print("Arm Up")
        self.robot.arm_and_claw.raise_arm()
    def Arm_Down(self):
        print("Arm Down")
        self.robot.arm_and_claw.lower_arm()
    def Left(self):
        print("Left 0 600")
        self.robot.drive_system.go(0,600)
    def Right(self):
        print("Right 0 600")
        self.robot.drive_system.go(600,0)
    def Stop(self):
        print('Stop')
        self.robot.drive_system.stop()
    def Quit(self):
        print("Quit")

def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    robot = bot.RoseBot()
    #robot.arm_and_claw.calibrate_arm()
    robot.arm_and_claw.raise_arm()
    #robot.arm_and_claw.lower_arm()
    #robot.arm_and_claw.move_arm_to_position(8)

    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    while True:
        time.sleep(0.01)  # Time to allow message processing




# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()