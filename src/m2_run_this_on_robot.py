"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Katana Colledge.
  Winter term, 2018-2019.
"""

import rosebot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot
import m2_Sprint3_delegate


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    #test_go(70,70)
    #test_stop()
    #test_go_straight_for_seconds()
    #test_go_straight_for_inches_using_time()
    #test_go_straight_for_inches_using_encoder()
    #real_thing()
    #test_distance()
    gui()






def gui():
    robot = rosebot.RoseBot()
    delegate=m2_Sprint3_delegate.DelegateThatReceives(robot)
    mqtt_reciever=com.MqttClient(delegate)
    mqtt_reciever.connect_to_pc()
    while True:
        time.sleep(0.01)
        if delegate.is_Quit()==1:
            print("Quit Sucessful")
            break;

def test_distance():
    robot = rosebot.RoseBot()
    robot.drive_system.go_forward_until_distance_is_less_than(5,100)
    #robot.drive_system.go_backward_until_distance_is_greater_than(5,25)
    #robot.drive_system.go_until_distance_is_within(1,3,25)

def test_go_straight_for_inches_using_encoder():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_encoder(10,100)
    robot.drive_system.go_straight_for_inches_using_encoder(10,-100)
    robot.drive_system.go_straight_for_inches_using_encoder(20,100)
    robot.drive_system.go_straight_for_inches_using_encoder(20,-100)

#def test_go(speed1, speed2):
 #   robot = rosebot.RoseBot()
 #   robot.drive_system.go(speed1,speed2)

#def test_stop():

    robot = rosebot.RoseBot()
    robot.drive_system.stop()

def test_go_straight_for_seconds():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_seconds(5, 100)
    robot.drive_system.go_straight_for_seconds(5,-100)
    robot.drive_system.go_straight_for_seconds(0,10)
    robot.drive_system.go_straight_for_seconds(3,20)
    robot.drive_system.go_straight_for_seconds(3,0)
    robot.drive_system.go_straight_for_seconds(3,-20)

def test_go_straight_for_inches_using_time():
    robot = rosebot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_time(10,100)
    robot.drive_system.go_straight_for_inches_using_time(10,-100)
    robot.drive_system.go_straight_for_inches_using_time(5,25)
    robot.drive_system.go_straight_for_inches_using_time(0,75)
    robot.drive_system.go_straight_for_inches_using_time(3,60)

#def real_thing():
 #   robot=rosebot.RoseBot()
  #  delegate = shared_gui_delegate_on_robot.DelegateThatReceives
   # mqtt_reciever = com.MqttClient(delegate)
    #mqtt_reciever.connect_to_pc()

   # while True:
    #    if delegate.stop_program:
     #       break
      #  time.sleep(0.01)


#




# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()