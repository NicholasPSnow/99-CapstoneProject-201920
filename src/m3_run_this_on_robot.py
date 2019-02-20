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
    # run_test_pid()


def real_thing():
    robot = bot.RoseBot()
    pid = extra.PID(1, 0, 0, 0.1, 0)
    delegate = gui_delegate.DelegateThatReceives(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()
    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_pc()
    while True:
        time.sleep(0.01)

# -------------------------------------------------------------------------
# Test Functions
# -------------------------------------------------------------------------


def run_test_camera():
    robot = bot.RoseBot()
    robot.drive_system.spin_clockwise_until_sees_object(25, 10)
    time.sleep(3)
    robot.drive_system.spin_counterclockwise_until_sees_object(25, 10)


def run_test_ir(n):
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
    robot = bot.RoseBot()
    robot.arm_and_claw.calibrate_arm()
    pos = [14, 2, 10, 3]
    for i in pos:
        robot.arm_and_claw.move_arm_to_position(pos[i])


def run_test_drive_inches_using_encoder():
    robot = bot.RoseBot()
    robot.drive_system.go_straight_for_inches_using_encoder(5, 50)
    time.sleep(3)
    robot.drive_system.go_straight_for_inches_using_encoder(12, 50)


def run_test_pid():
    robot = bot.RoseBot()


def run_mqtt_test(mqtt_sender):
    mqtt_sender.send_message("print_message", ["test successful"])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
