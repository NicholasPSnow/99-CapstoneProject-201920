import time

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

    robot.led_system.left_led.turn_off()
    robot.led_system.right_led.turn_off()
    robot.drive_system.go(25, 25)
    print("Checkpoint 1")

    while average > 5:
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
        distance.pop(0)
        average = average_list(distance)
        # print(state, average)
        state, last_state = update_state(last_state, initial_dist, average, init_rate, acceleration, state)
        led_cycle(robot, state)

    robot.drive_system.stop()
    robot.arm_and_claw.raise_arm()

def update_state(last_state, initial_dist, current_dist, init_rate, acceleration, state):
    cycle_time = (1.0 / float(init_rate)) - ((initial_dist - current_dist) / float(acceleration))
    print(state, cycle_time)
    if cycle_time < 0.1:
        cycle_time = 0.1
    if (time.time() - last_state) >= cycle_time:

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
        robot.led_system.right_led.turn_off()
    elif state == 1:
        robot.led_system.left_led.turn_off()
        robot.led_system.right_led.turn_on()
    elif state == 2:
        robot.led_system.left_led.turn_on()
        robot.led_system.right_led.turn_on()
    else:
        robot.led_system.left_led.turn_off()
        robot.led_system.right_led.turn_off()

# -------------------------------------------------------------------------
# Feature 10
# -------------------------------------------------------------------------


def feature_10(robot, speed, direction):
    print('speed:', speed, type(speed))
    speed = int(speed)
    print('speed:', speed, type(speed))
    print('direction:', direction, direction[0])
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

    feature_9(robot, 0.1, 1)
