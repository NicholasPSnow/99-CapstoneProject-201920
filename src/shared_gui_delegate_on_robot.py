"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Nicholas Snow, Katana Colledge, and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import math
import shared_gui

class DelegateThatReceives(object):

    def __init__(self, robot):
        self.robot = robot

    def command(self):
        pass

    def movement(self, left_speed, right_speed):
        self.robot.drive_system.go(int(left_speed), int(right_speed))

    def arm_movement(self, command):
        method_dict = {}

    """
    def arm_up(self):
        print("Arm Up")
        self.robot.arm_and_claw.raise_arm()

    def arm_down(self):
        print("Arm Down")
        self.robot.arm_and_claw.lower_arm()

    def left(self):
        print("Left 0 600")
        self.robot.drive_system.go(0, 600)

    def right(self):
        print("Right 0 600")
        self.robot.drive_system.go(600, 0)

    def stop(self):
        print('Stop')
        self.robot.drive_system.stop()

    def quit(self):
        print("Quit")
    """
