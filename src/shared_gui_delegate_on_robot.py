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


class DelegateThatReceives(object):

    def __init__(self, robot):
        self.robot = bot.RoseBot()

    ##DRIVE SYSTEM
    #Handle Quit and Exit
    def command(self,argument):
        print("Command Recieved: ",argument)
        if argument == "quit":
            pass
        if argument == 'exit':
            pass

    def stop(self):
        print("Command Recieved: Stop")
        self.robot.drive_system.stop()


    #Handle Forward and Backward and Left and Right
    def movement(self, left_speed, right_speed):
        print("Command Recieved: Movement",left_speed,right_speed)
        self.robot.drive_system.go(int(left_speed), int(right_speed))

    ##ARM SYSTEM
    def arm_movement(self, command, pos=0):
        print("Command Recieved: ",command)
        method_dict = {'up': self.robot.arm_and_claw.raise_arm, 'move_to_pos': self.robot.arm_and_claw.move_arm_to_position,
                       'calibrate': self.robot.arm_and_claw.calibrate_arm, 'down': self.robot.arm_and_claw.lower_arm}
        if command == 'move_to_pos':
            method_dict['move_to_pos'](pos)
        else:
            method_dict[command]()

    ##Sprint 1 SYSTEM

    def Forward_Time(self,speed,time):
        print("Command Recieved: Forward_Time")
        self.robot.drive_system.go_straight_for_seconds(time,speed)
    def Forward_Time_Inches(self,speed,inches):
        print("Command Recieved: Forward_Time_Inches")
        self.robot.drive_system.go_straight_for_inches_using_time(inches,speed)
    def Forward_Inches(self,speed,inches):
        print("Command Recieved: Forward_Inches")
        self.robot.drive_system.go_straight_for_inches_using_encoder(self,inches,speed)

    def beep_button(self,numberofbeeps):
        print("Command Recieved: Beep")
        for k in range(int(numberofbeeps)):
            self.robot.SoundSystem.beeper
    def tone_button(self,duration,frequency):
        print("Command Recieved: Tone")
        self.robot.SoundSystem.tone_maker(frequency,duration)
    def speak_button(self,text):
        print("Command Recieved: Speak")
        self.robot.SoundSystem.speech_maker(text)