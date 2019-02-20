"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework) and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot as gui_delegate
import m3_extra as extra


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    real_thing()
    # run_test_ir(0)
    # run_test_arm()
    # run_test_camera()


def real_thing():
    """
    allows the robot to be controlled through the gui on the pc
    """
    robot = bot.RoseBot()
    robot.end = 0
    delegate = gui_delegate.DelegateThatReceives(robot)
    mqtt_receiver = com.MqttClient(delegate)
    delegate.m3_sender = com.MqttClient()
    mqtt_receiver.connect_to_pc()
    delegate.m3_sender.connect_to_pc()
    delegate.pid = extra.PID(1, 0, 0, 0.1, 0)  # the PID for line following, I and D values are currently disabled

    while True:
        time.sleep(0.01)

# -------------------------------------------------------------------------
# Test Functions
# -------------------------------------------------------------------------


def run_test_camera():
    """
    tests the sprint 2 camera functions
    """
    robot = bot.RoseBot()
    robot.drive_system.spin_clockwise_until_sees_object(25, 10)
    time.sleep(3)
    robot.drive_system.spin_counterclockwise_until_sees_object(25, 10)


def run_test_ir(n):
    """
    tests the sprint 2 proximity sensor functions, 1 makes a beep if it detects an object within 20 in.
    :param n: switches which test is used
    """
    robot = bot.RoseBot()
    if n == 1:
        robot.drive_system.go_forward_until_distance_is_less_than(6, 25)
        time.sleep(5)
        robot.drive_system.go_backward_until_distance_is_greater_than(6, 25)
        time.sleep(5)
        robot.drive_system.go_until_distance_is_within(6, 25)
        time.sleep(5)
        robot.drive_system.go_until_distance_is_within(6, 25)
    else:
        a = time.time()
        robot.drive_system.go(100, 100)
        while time.time() - a < 5:
            if robot.sensor_system.ir_proximity_sensor.get_distance() < 20:
                robot.sound_system.beeper.beep()
        robot.drive_system.stop()


def run_test_arm():
    """
    tests the sprint 1 robot arm functions
    """
    robot = bot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    pos = [14, 2, 10, 3]
    for i in pos:
        robot.arm_and_claw.move_arm_to_position(pos[i])


def run_test_drive_inches_using_encoder():
    """
    tests the sprint 1 drive functions
    """
    robot = bot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_encoder(5, 50)
    time.sleep(3)
    robot.drive_system.go_straight_for_inches_using_encoder(12, 50)


def run_mqtt_test(mqtt_sender):
    """
    tests if the robot can send commands to the pc
    :param mqtt_sender: the mqtt client used to send commands on the robot
    """
    mqtt_sender.send_message("print_message", ["test successful"])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
