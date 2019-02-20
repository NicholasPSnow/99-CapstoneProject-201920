"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Katana Colledge.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import time
import math
import rosebot

class DelegateThatReceives(object):

    def __init__(self, robot):
        self.robot = rosebot.RoseBot()
        self.Quit=0
        self.Exit=0

    def is_Quit(self):
        if self.Quit==1:
            self.robot.drive_system.stop()
            self.robot.arm_and_claw.lower_arm()
        return self.Quit

    def establish_link_button(self):
        print("Command Recieved: Establish Link")
        self.robot.arm_and_claw.calibrate_arm()
        self.robot.sound_system.beeper.beep()
        self.robot.sound_system.beeper.beep()

    def status_button(self):
        print("Command Recieved: Checking Systems")
        color = self.robot.sensor_system.color_sensor.get_color()
        print(color)
        if color == 'Blue':
            self.robot.drive_system.go_straight_until_color_is_not(color,-100)
            print('Ship/has/been/breached/STOP')
        else:
            print('Ship/is/secure/STOP')

    def periscope_button(self):
        print('Command Recieved: Using periscope')
        self.robot.arm_and_claw.lower_arm()
        self.robot.arm_and_claw.raise_arm()
        self.robot.arm_and_claw.move_arm_to_position(20)
        self.robot.drive_system.spin_counterclockwise_until_sees_object(50,20)
        print('Message from crew incoming...',end='')
        time.sleep(3)
        print('there/is/something/out/there/STOP')
        time.sleep(3)
        self.robot.arm_and_claw.raise_arm()
        self.robot.arm_and_claw.lower_arm()


    def evacuate_button(self):
        print('Command Recieved: evacuating')
        escape = 0
        while True:
            self.robot.drive_system.go(100, 100)
            color = self.robot.sensor_system.color_sensor.get_color()
            blob = self.robot.sensor_system.camera.get_biggest_blob()
            blob_area = blob.width * blob.height
            if color != 'Blue':
                while True:
                    if blob_area <= 10:
                        break
                    if color == 'Blue':
                        break
                    print('spotted')
                    self.robot.drive_system.stop()
                    self.robot.drive_system.rotate_left(90)
                    blob = self.robot.sensor_system.camera.get_biggest_blob()
                    blob_area = blob.width * blob.height
                    color = self.robot.sensor_system.color_sensor.get_color()
            if color == 'Blue':
                print('In water')
                while True:
                    if blob_area <= 10:
                        break
                    if color != 'Blue':
                        escape = 1
                        break
                    print('spotted')
                    self.robot.drive_system.stop()
                    self.robot.drive_system.rotate_left(90)
                    blob = self.robot.sensor_system.camera.get_biggest_blob()
                    blob_area = blob.width * blob.height
                    color = self.robot.sensor_system.color_sensorget_color()
            if escape == 1:
                break
        print('Escape Successful')


    #morus code spits out code and message appears on screen

    #responds to certain commands





