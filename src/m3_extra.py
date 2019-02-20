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

# -------------------------------------------------------------------------
# Sprint 3
# -------------------------------------------------------------------------


def sprint_3(robot, pid, sender):
    pid.last_time = time.time()
    delta = 0
    point_list = []
    start_time = time.time()
    time_offset = 0
    while (time.time() - start_time) < 60:
        new = pid.update_output(int(robot.sensor_system.color_sensor.get_reflected_light_intensity()))
        if new is not None:
            delta = new
            if len(point_list) < 700:
                sender.send_message('graph_data', [(time.time() - pid.start_time - time_offset, delta)])
        robot.drive_system.left_motor.turn_on(limit_speed(20 + delta))
        robot.drive_system.right_motor.turn_on(limit_speed(20 - delta))
        if get_distance(robot) < 10:
            offset_start = time.time()
            get_object(robot)
            time_offset = time.time() - offset_start
    robot.drive_system.stop()
    sender.send_message('draw_graph', [])


def get_object(robot):  # init_rate is cycles per second
    robot.drive_system.go(20, 20)
    time.sleep(2)

    robot.drive_system.stop()
    robot.arm_and_claw.raise_arm()
    robot.drive_system.go(-30, 30)
    time.sleep(3)
    robot.drive_system.stop()

    robot.drive_system.go(50, 50)
    time.sleep(2)
    robot.drive_system.stop()
    robot.arm_and_claw.lower_arm()
    robot.drive_system.go(-50, -50)
    time.sleep(2)
    robot.drive_system.stop()

    robot.drive_system.go(30, -30)
    time.sleep(3)
    robot.drive_system.stop()


def get_distance(robot):
    distance = []  # acceleration is cycles per second per inch
    for _ in range(10):
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
    average = average_list(distance)
    return average


def limit_speed(n):
    if n > 100:
        n = 100
    elif n < -100:
        n = -100
    return n


class PID(object):
    def __init__(self, kp, ki, kd, interval, set_point):
        self.Kp = kp
        self.Ki = ki
        self.Kd = kd
        self.last_time = time.time()
        self.start_time = self.last_time
        self.interval = interval
        self.set_point = set_point
        self.proportional = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0

    def update_output(self, current_value):
        if time.time() - self.last_time >= self.interval:
            dt = time.time() - self.last_time
            error = self.set_point - current_value

            self.proportional = self.Kp * error
            self.integral = self.integral + self.Ki * error * dt
            self.derivative = self.Kd * (error - self.last_error) / dt

            self.last_error = error
            self.last_time = time.time()

            output = self.proportional + self.integral + self.derivative

            return output

    def clear(self):
        self.__init__(self.Kp, self.Ki, self.Kd, self.interval, self.set_point)
