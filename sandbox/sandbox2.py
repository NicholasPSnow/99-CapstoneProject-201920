# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

def go_straight_for_inches_using_encoder(inches, speed):
    """
    Makes the robot go straight (forward if speed > 0, else backward)
    at the given speed for the given number of inches,
    using the encoder (degrees traveled sensor) built into the motors.
    """
    inches_per_degree = 30 / 360
    degree = inches / inches_per_degree
    left_motor
    self.go(speed, speed)
    while True:
        position = self.left_motor.get_position()
        if abs(position) >= degree:
            break
    self.stop()