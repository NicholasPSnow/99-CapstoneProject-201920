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
#import shared_gui_delegate_on_robot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    robot = bot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    print('Calibrated')
    robot.arm_and_claw.raise_arm()
    print('raise')
    robot.arm_and_claw.lower_arm()
    print('lower')
    robot.arm_and_claw.move_arm_to_position(14.2 * 8)
    print('moveto')


def real():
    robot = bot.RoseBot()
    delegate=shared_gui_delegate_on_robot(robot)
    mqtt_reciever=com.MqttClient(delegate)
    mqtt_reciever.connect_to_pc()
    while True:
        time.sleep(0.01)

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()