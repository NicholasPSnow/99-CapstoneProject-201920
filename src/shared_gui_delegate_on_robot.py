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

    def command(self):  # this should handle stop and quit
        pass

    def movement(self, left_speed, right_speed):
        self.robot.drive_system.go(int(left_speed), int(right_speed))

    def arm_movement(self, command, pos=0):
        method_dict = {'up': self.robot.arm_and_claw.raise_arm, 'move_to_pos': self.robot.arm_and_claw.move_arm_to_position,
                       'calibrate': self.robot.arm_and_claw.calibrate_arm, 'down': self.robot.arm_and_claw.lower_arm}
        if command == 'move_to_pos':
            method_dict['move_to_pos'](pos)
        else:
            method_dict[command]()
