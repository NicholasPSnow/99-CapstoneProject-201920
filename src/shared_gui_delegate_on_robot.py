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
        self.robot = bot.RoseBot()

    ##DRIVE SYSTEM
    #Handle Quit and Exit
    def command(self,argument):
        if argument == "quit":
            pass
        if argument == 'exit':
            pass

    def stop(self):
        self.robot.drive_system.stop()


    #Handle Forward and Backward and Left and Right
    def movement(self, left_speed, right_speed):
        self.robot.drive_system.go(int(left_speed), int(right_speed))

    ##ARM SYSTEM
    def arm_movement(self, command, pos=0):
        method_dict = {'up': self.robot.arm_and_claw.raise_arm, 'move_to_pos': self.robot.arm_and_claw.move_arm_to_position,
                       'calibrate': self.robot.arm_and_claw.calibrate_arm, 'down': self.robot.arm_and_claw.lower_arm}
        if command == 'move_to_pos':
            method_dict['move_to_pos'](pos)
        else:
            method_dict[command]()

    ##Sprint 1 SYSTEM

    def Forward_Time(self,speed,time):
        self.robot.drive_system.go_straight_for_seconds(time,speed)
    def Forward_Time_Inches(self,speed,inches):
        self.robot.drive_system.go_straight_for_inches_using_time(inches,speed)
    def Forward_Inches(self,speed,inches):
        self.robot.drive_system.go_straight_for_inches_using_encoder(self,inches,speed)
    def beep_button(self,numberofbeeps):
        for k in range(int(numberofbeeps)):
            self.robot.SoundSystem.beeper

    def tone_button(self,duration,frequency):
        self.robot.SoundSystem.tone_maker(frequency,duration)
    def speak_button(self,text):
        self.robot.SoundSystem.speech_maker(text)