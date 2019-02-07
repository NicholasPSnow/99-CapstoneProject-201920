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
import shared_gui_delegate_on_robot

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


