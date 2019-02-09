"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot as gui_delegate
import rosebot


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """
    # real_thing()
    run_test_ir()

def real_thing():
    robot = bot.RoseBot()
    delegate = gui_delegate.DelegateThatReceives()
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)


def run_test_ir():
    robot = bot.RoseBot()
    """
    robot.drive_system.go_forward_until_distance_is_less_than(6, 25)
    time.sleep(5)
    robot.drive_system.go_backward_until_distance_is_greater_than(6, 25)
    time.sleep(5)
    robot.drive_system.go_until_distance_is_within(6, 25)
    time.sleep(5)
    robot.drive_system.go_until_distance_is_within(6, 25)
    """
    a = time.time()
    robot.drive_system.go(100, 100)
    while time.time() - a < 5000:
        if robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() < 12:
            robot.sound_system.beeper.beep()
    robot.drive_system.stop()


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
