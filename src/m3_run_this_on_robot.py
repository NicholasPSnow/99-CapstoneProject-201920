"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework) and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import shared_gui_delegate_on_robot as gui_delegate


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
    robot = bot.RoseBot()
    delegate = gui_delegate.DelegateThatReceives(robot)
    mqtt_receiver = com.MqttClient(delegate)
    mqtt_receiver.connect_to_pc()

    while True:
        time.sleep(0.01)


# -------------------------------------------------------------------------
# Sprint 2 Functions
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Feature 9
# -------------------------------------------------------------------------

def feature_9(robot, init_rate, acceleration):  # init_rate is cycles per second
    distance = []                               # acceleration is cycles per second per inch
    last_state = time.time()
    for _ in range(10):
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
    average = average_list(distance)
    initial_dist = average
    state = 0

    robot.drive_system.go(25, 25)

    while average > 1:
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
        distance.pop(0)
        average = average_list(distance)
        state, last_state = update_state(last_state, initial_dist, average, init_rate, acceleration, state)
        led_cycle(robot, state)

    robot.drive_system.stop()
    robot.arm_and_claw.raise_arm()


def update_state(last_state, initial_dist, current_dist, init_rate, acceleration, state):
    cycle_time = (1.0 / init_rate) - ((initial_dist - current_dist) / acceleration)
    if cycle_time < 0.1:
        cycle_time = 0.1
    if (last_state - time.time()) >= cycle_time:

        return (state + 1) % 4, time.time()

    return state, last_state


def average_list(list1):
    average = 0
    for i in list1:
        average = average + i

    return average / len(list1)


def led_cycle(robot, state):
    if state == 0:
        robot.led_system.left_led.turn_on()
    elif state == 1:
        robot.led_system.left_led.turn_off()
        robot.led_system.right_led.turn_on()
    elif state == 2:
        robot.led_system.left_led.turn_on()
    else:
        robot.led_system.left_led.turn_oof()
        robot.led_system.left_led.turn_off()

# -------------------------------------------------------------------------
# Feature 10
# -------------------------------------------------------------------------


def feature_10(robot, speed, direction):
    if direction[0] == 'selected':
        speed = speed * -1

    robot.drive_system.left_motor.turn_on(speed)
    robot.drive_system.right_motor.turn_on(-1 * speed)

    while True:
        blob = robot.sensor_system.camera.get_biggest_blob()
        blob_area = blob.width * blob.height

        if blob_area >= 4 and 139 < blob.center.x < 180:
            robot.drive_system.stop()
            break

    feature_9(robot, 0.5, 0.1)


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

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
