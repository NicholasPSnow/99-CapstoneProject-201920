"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Katana Colledge.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    test_go(100)
    #test_stop()
    #test_go_straight_for_seconds()
    #test_go_straight_for_inches_using_time()

def test_go(speed):
    robot = rosebot.roseBot()
    robot.go(speed)

def test_stop():
    robot = rosebot.roseBot()
    robot.stop()

def test_go_straight_for_seconds():
    robot = rosebot.roseBot()
    robot.go_straight_for_seconds(5, 100)
    robot.go_straight_for_seconds(5,-100)
    robot.go_straight_for_seconds(0,10)
    robot.go_straight_for_seconds(3,20)
    robot.go_straight_for_seconds(3,0)
    robot.go_straight_for_seconds(3,-20)

def test_go_straight_for_inches_using_time():
    robot = rosebot.roseBot()
    robot.go_straight_for_inches_using_time(10,100)
    robot.go_straight_for_inches_using_time(10,-100)
    robot.go_straight_for_inches_using_time(5,25)
    robot.go_straight_for_inches_using_time(0,75)
    robot.go_straight_for_inches_using_time(3,60)






# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()