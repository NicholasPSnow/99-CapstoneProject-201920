"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    run_test_arm()


def run_test_arm():
    robot = bot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    pos = [14, 2, 10, 3]
    for i in pos:
        robot.arm_and_claw.move_arm_to_position(pos[i])
    # robot.arm_and_claw.calibrate_arm()
    # robot.arm_and_claw.raise_arm()

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()