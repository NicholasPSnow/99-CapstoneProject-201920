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
import shared_gui
import shared_gui_delegate_on_robot

def DelegateThatReceives(robot):
    return shared_gui_delegate_on_robot(robot)

def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    robot = bot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    robot.arm_and_claw.raise_arm()
    robot.arm_and_claw.lower_arm()
    robot.arm_and_claw.move_arm_to_position(14.2*8)

    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")

    my_delegate = DelegateThatReceives(robot)
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    #while True:
        #time.sleep(0.01)  # Time to allow message processing




# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()