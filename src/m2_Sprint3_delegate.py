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


def handle_establish_link_button(self):
    print("Command Recieved: Establish Link")
    rosebot.ArmAndClaw.calibrate_arm()
    rosebot.SoundSystem.beeper.beep()
    rosebot.SoundSystem.beeper.beep()

def handle_status_button(self):
    print("Command Recieved: Checking Systems")
    color = rosebot.ColorSensor.get_color()
    print(color)
    if color != 'Blue':
        return ('Ship/has/been/breached/STOP')
    else:
        return('Ship/is/secure/STOP')

#morus code spits out code and message appears on screen

#responds to certain commands





