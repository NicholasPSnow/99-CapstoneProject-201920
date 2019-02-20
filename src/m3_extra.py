import time

# -------------------------------------------------------------------------
# Sprint 2 Functions
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------
# Feature 9
# -------------------------------------------------------------------------


def feature_9(robot, init_rate, acceleration):
    """
    runs feature 9
    :param robot: the robot the function is running on
    :param init_rate: cycles per second
    :param acceleration: cycles per second per inch
    """
    distance = []
    last_state = time.time()
    for _ in range(10):  # averages the output of the last 10 readings
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
    average = average_list(distance)
    initial_dist = average
    state = 0

    robot.led_system.left_led.turn_off()
    robot.led_system.right_led.turn_off()
    robot.drive_system.go(25, 25)

    while average > 5:  # removes the oldest reading when a new one is added
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
        distance.pop(0)
        average = average_list(distance)
        state, last_state = update_state(last_state, initial_dist, average, init_rate, acceleration, state)
        led_cycle(robot, state)  # updates the leds

    robot.drive_system.stop()
    robot.arm_and_claw.raise_arm()


def update_state(last_state, initial_dist, current_dist, init_rate, acceleration, state):
    """
    updates the leds
    :param last_state: the last time the led state changed
    :param initial_dist: the starting distance from the object
    :param current_dist: the current distance from the object
    :param init_rate: the starting rate of change of led states
    :param acceleration: how quickly the led state changing increases with distance
    :param state: the current led state
    """
    cycle_time = (1.0 / float(init_rate)) - ((initial_dist - current_dist) / float(acceleration))
    if cycle_time < 0.1:
        cycle_time = 0.1
    if (time.time() - last_state) >= cycle_time:

        return (state + 1) % 4, time.time()  # increments the led state if enough time has passed

    return state, last_state  # keeps the same led state if not enough time has passed


def average_list(list1):
    """
    averages a list of numbers
    :param list1: a list of numbers
    """
    average = 0
    for i in list1:
        average = average + i

    return average / len(list1)


def led_cycle(robot, state):
    """
    changes the robot's leds to the input state
    :param robot: the robot to run this on
    :param state: the desired led state
    """
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
    """
    runs feature 10
    :param robot: the robot the function runs on
    :param speed: the spinning speed
    :param direction: the direction to spin, checked is cw, unchecked is ccw
    """
    speed = int(speed)
    if direction[0] == 'selected':  # changes the spin direction if a checkbox on the gui is checked
        speed = speed * -1

    robot.drive_system.left_motor.turn_on(speed)
    robot.drive_system.right_motor.turn_on(-1 * speed)

    while True:  # waits until a large enough blob is close to the center of the camera's fov
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
    """
    makes the robot follow a line, picking up and moving blocks along the way
    :param robot: the robot this is run on
    :param pid: a pid object, used to control the motors for line following
    :param sender: the mqtt client used to send graph points from the robot to the pc
    """
    pid.last_time = time.time()
    delta = 0  # the motor speed offset
    point_list = []
    start_time = time.time()
    time_offset = 0
    while (time.time() - start_time) < 60:  # runs for 60 seconds
        new = pid.update_output(int(robot.sensor_system.color_sensor.get_reflected_light_intensity()))
        if new is not None:  # the pid returns none if not enough time has passed since the last pid output
            delta = new
            if len(point_list) < 700:
                sender.send_message('graph_data', [(time.time() - pid.start_time - time_offset, delta)])
                # the time since starting sprint_3 and the current motor speed offset are sent as point to the pc
        robot.drive_system.left_motor.turn_on(limit_speed(20 + delta))
        robot.drive_system.right_motor.turn_on(limit_speed(20 - delta))
        if get_distance(robot) < 10:  # if an object is close enough, move it out of the way
            offset_start = time.time()
            get_object(robot)
            time_offset = time.time() - offset_start
    robot.drive_system.stop()
    sender.send_message('draw_graph', [])  # tells the pc that the robot is done and to start drawing the graph


def get_object(robot):
    """
    makes the robot pick up objects and move them to the left before returning to the line
    """
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
    """
    returns the distance from the nearest object in front of the robot
    """
    distance = []
    for _ in range(10):
        distance.append(robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())
    average = average_list(distance)
    return average


def limit_speed(n):
    """
    prevents the motor speed from going too high or low
    :param n: the speed
    :return:
    """
    if n > 100:
        n = 100
    elif n < -100:
        n = -100
    return n


class PID(object):
    """
    a pid used for line following
    """
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
        """
        calculates the new value for the motor speed offset
        :param current_value: the current color sensor value
        """
        if time.time() - self.last_time >= self.interval:  # waits until enough time has passed since the last reading
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
        """
        resets the pid
        """
        self.__init__(self.Kp, self.Ki, self.Kd, self.interval, self.set_point)
