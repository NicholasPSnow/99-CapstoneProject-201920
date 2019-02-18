"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Katana Colledge.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import math


def establish_link_button(self):
    print("Command Recieved: Establish Link")
    rosebot.ArmAndClaw.calibrate_arm()
    rosebot.SoundSystem.beeper.beep()
    rosebot.SoundSystem.beeper.beep()

def status_button(self):
    print("Command Recieved: Checking Systems")
    color = rosebot.ColorSensor.get_color()
    print(color)
    if color == 'Blue':
        rosebot.DriveSystem.go_straight_until_color_is_not(color,-100)
        print('Ship/has/been/breached/STOP')
    else:
        print('Ship/is/secure/STOP')

def periscope_button(self):
    print('Command Recieved: Using periscope')
    rosebot.ArmAndClaw.lower_arm()
    rosebot.ArmAndClaw.raise_arm()
    rosebot.ArmAndClaw.move_arm_to_position(20)
    rosebot.DriveSystem.spin_counterclockwise_until_sees_object(50,20)
    print('Message from crew incoming...',end='')
    time.sleep(3)
    print('there/is/something/out/there/STOP')
    time.sleep(3)
    rosebot.ArmAndClaw.raise_arm()
    rosebot.ArmAndClaw.lower_arm()


def evacuate_button(self):
    print('Command Recieved: evacuating')
    escape = 0
    while True:
        rosebot.DriveSystem.go(100, 100)
        color = rosebot.ColorSensor.get_color()
        blob = self.sensor_system.camera.get_biggest_blob()
        blob_area = blob.width * blob.height
        if color != 'Blue':
            while True:
                if blob_area <= 10:
                    break
                if color == 'Blue':
                    break
                print('spotted')
                self.stop()
                rosebot.DriveSystem.rotate_left(90)
                blob = self.sensor_system.camera.get_biggest_blob()
                blob_area = blob.width * blob.height
                color = rosebot.ColorSensor.get_color()
        if color == 'Blue':
            print('In water')
            while True:
                if blob_area <= 10:
                    break
                if color != 'Blue':
                    escaped = 1
                    break
                print('spotted')
                self.stop()
                rosebot.DriveSystem.rotate_left(90)
                blob = self.sensor_system.camera.get_biggest_blob()
                blob_area = blob.width * blob.height
                color = rosebot.ColorSensor.get_color()
        if escape == 1:
            break
    print('Escape Successful')


#morus code spits out code and message appears on screen

#responds to certain commands





