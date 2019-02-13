"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Constructs and returns Frame objects for the basics:
  -- teleoperation
  -- arm movement
  -- stopping the robot program

  This code is SHARED by all team members.  It contains both:
    -- High-level, general-purpose methods for a Snatch3r EV3 robot.
    -- Lower-level code to interact with the EV3 robot library.

  Author:  Your professors (for the framework and lower-level code)
    and Nicholas Snow, Katana College, and Zach Kelly.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk
import time


def get_teleoperation_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Teleoperation")
    left_speed_label = ttk.Label(frame, text="Left wheel speed (0 to 100)")
    right_speed_label = ttk.Label(frame, text="Right wheel speed (0 to 100)")

    left_speed_entry = ttk.Entry(frame, width=8)
    left_speed_entry.insert(0, "100")
    right_speed_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "100")

    forward_button = ttk.Button(frame, text="Forward")
    backward_button = ttk.Button(frame, text="Backward")
    left_button = ttk.Button(frame, text="Left")
    right_button = ttk.Button(frame, text="Right")
    stop_button = ttk.Button(frame, text="Stop")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    left_speed_label.grid(row=1, column=0)
    right_speed_label.grid(row=1, column=2)
    left_speed_entry.grid(row=2, column=0)
    right_speed_entry.grid(row=2, column=2)

    forward_button.grid(row=3, column=1)
    left_button.grid(row=4, column=0)
    stop_button.grid(row=4, column=1)
    right_button.grid(row=4, column=2)
    backward_button.grid(row=5, column=1)

    # Set the button callbacks:
    forward_button["command"] = lambda: handle_forward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    backward_button["command"] = lambda: handle_backward(
        left_speed_entry, right_speed_entry, mqtt_sender)
    left_button["command"] = lambda: handle_left(
        left_speed_entry, right_speed_entry, mqtt_sender)
    right_button["command"] = lambda: handle_right(
        left_speed_entry, right_speed_entry, mqtt_sender)
    stop_button["command"] = lambda: handle_stop(mqtt_sender)

    return frame


def get_arm_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Entry and Button objects that control the EV3 robot's Arm
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Arm and Claw")
    position_label = ttk.Label(frame, text="Desired arm position:")
    position_entry = ttk.Entry(frame, width=8)

    raise_arm_button = ttk.Button(frame, text="Raise arm")
    lower_arm_button = ttk.Button(frame, text="Lower arm")
    calibrate_arm_button = ttk.Button(frame, text="Calibrate arm")
    move_arm_button = ttk.Button(frame,
                                 text="Move arm to position (0 to 5112)")
    blank_label = ttk.Label(frame, text="")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    position_label.grid(row=1, column=0)
    position_entry.grid(row=1, column=1)
    position_entry.insert(0, "0")
    move_arm_button.grid(row=1, column=2)

    blank_label.grid(row=2, column=1)
    raise_arm_button.grid(row=3, column=0)
    lower_arm_button.grid(row=3, column=1)
    calibrate_arm_button.grid(row=3, column=2)

    # Set the Button callbacks:
    raise_arm_button["command"] = lambda: handle_raise_arm(mqtt_sender)
    lower_arm_button["command"] = lambda: handle_lower_arm(mqtt_sender)
    calibrate_arm_button["command"] = lambda: handle_calibrate_arm(mqtt_sender)
    move_arm_button["command"] = lambda: handle_move_arm_to_position(position_entry.get(), mqtt_sender)

    return frame


def get_control_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame has
    Button objects to exit this program and/or the robot's program (via MQTT).
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Control")
    quit_robot_button = ttk.Button(frame, text="Stop the robot's program")
    exit_button = ttk.Button(frame, text="Stop this and the robot's program")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    quit_robot_button.grid(row=1, column=0)
    exit_button.grid(row=1, column=2)

    # Set the Button callbacks:
    quit_robot_button["command"] = lambda: handle_quit(mqtt_sender)
    exit_button["command"] = lambda: handle_exit(mqtt_sender)

    return frame

###############################################################################
###############################################################################
# The following specifies, for each Button,
# what should happen when the Button is pressed.
###############################################################################
###############################################################################

###############################################################################
# Handlers for Buttons in the Teleoperation frame.
###############################################################################
def handle_forward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    with the speeds used as given.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print('forward', left_entry_box.get(), right_entry_box.get())
    mqtt_sender.send_message('movement', [left_entry_box.get(), right_entry_box.get()])


def handle_backward(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negatives of the speeds in the entry boxes.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print('backward', left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = -int(right_entry_box.get())
    mqtt_sender.send_message('movement', [str(left), str(right)])


def handle_left(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the left entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print('left', left_entry_box.get(), right_entry_box.get())
    left = -int(left_entry_box.get())
    right = int(right_entry_box.get())
    mqtt_sender.send_message('movement', [str(left), str(right)])

def handle_right(left_entry_box, right_entry_box, mqtt_sender):
    """
    Tells the robot to move using the speeds in the given entry boxes,
    but using the negative of the speed in the right entry box.
      :type  left_entry_box:   ttk.Entry
      :type  right_entry_box:  ttk.Entry
      :type  mqtt_sender:      com.MqttClient
    """
    print('right', left_entry_box.get(), right_entry_box.get())
    left = int(left_entry_box.get())
    right = -int(right_entry_box.get())
    mqtt_sender.send_message('movement', [str(left), str(right)])

def handle_stop(mqtt_sender):
    """
    Tells the robot to stop.
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message('stop')
    print("Stop")

###############################################################################
# Handlers for Buttons in the ArmAndClaw frame.
###############################################################################
def handle_raise_arm(mqtt_sender):
    """
    Tells the robot to raise its Arm until its touch sensor is pressed.
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message('up')
    print("Move Arm Up")

def handle_lower_arm(mqtt_sender):
    """
    Tells the robot to lower its Arm until it is all the way down.
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message('down')
    print("Move Arm Down")

def handle_calibrate_arm(mqtt_sender):
    """
    Tells the robot to calibrate its Arm, that is, first to raise its Arm
    until its touch sensor is pressed, then to lower its Arm until it is
    all the way down, and then to mark taht position as position 0.
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message('calibrate')
    print("Calibrate")

def handle_move_arm_to_position(position_entry, mqtt_sender):
    """
    Tells the robot to move its Arm to the position in the given Entry box.
    The robot must have previously calibrated its Arm.
      :type  arm_position_entry  ttk.Entry
      :type  mqtt_sender:        com.MqttClient
    """
    mqtt_sender.send_message('move_to_pos', [str(position_entry)])
    print("Move to Position:",position_entry)

###############################################################################
# Handlers for Buttons in the Control frame.
###############################################################################
def handle_quit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
      :type  mqtt_sender:  com.MqttClient
    """
    mqtt_sender.send_message('command', ['quit'])
    print('########')
    print('# Quit #')
    print('########')

def handle_exit(mqtt_sender):
    """
    Tell the robot's program to stop its loop (and hence quit).
    Then exit this program.
      :type mqtt_sender: com.MqttClient
    """
    mqtt_sender.send_message('command', ['exit'])
    print('########')
    print('# Exit #')
    print('########')




def get_Sprint_1_Drive_System_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Special objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Secondary Drive System")
    wheel_speed_label = ttk.Label(frame, text="Wheel Speed (0 to 100)")
    time_label = ttk.Label(frame, text="Movement Time (0 to INF)")
    inches_label = ttk.Label(frame, text="Movement Distance (0 to INF)")

    wheel_speed_entry = ttk.Entry(frame, width=8)
    wheel_speed_entry.insert(0, "100")
    time_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    time_entry.insert(0, "10")
    inches_entry = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    inches_entry.insert(0, "10")


    forward_time_button = ttk.Button(frame, text="Forward for Seconds")
    forward_time_inches_button = ttk.Button(frame, text="Forward for Inches(time)")
    forward_inches_button = ttk.Button(frame, text="Forward for Inches(Encoder)")


    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    wheel_speed_label.grid(row=1, column=0)
    time_label.grid(row=1, column=1)
    inches_label.grid(row=1, column=2)
    wheel_speed_entry.grid(row=2, column=0)
    time_entry.grid(row=2, column=1)
    inches_entry.grid(row=2, column=2)

    forward_time_button.grid(row=3, column=0)
    forward_time_inches_button.grid(row=3, column=1)
    forward_inches_button.grid(row=3, column=2)

    # Set the button callbacks:
    forward_time_button["command"] = lambda: handle_forward_time_button(wheel_speed_entry.get(), time_entry.get(), mqtt_sender)
    forward_time_inches_button["command"] = lambda: handle_forward_time_inches_button(wheel_speed_entry.get(), inches_entry.get(), mqtt_sender)
    forward_inches_button["command"] = lambda: handle_forward_inches_button(wheel_speed_entry.get(), inches_entry.get(), mqtt_sender)
    return frame


def handle_forward_time_button(speed,time,mqtt_sender):
    mqtt_sender.send_message('Forward_Time', [str(speed),str(time)])
    print('Forward_Time',speed,time)
def handle_forward_time_inches_button(speed,inches,mqtt_sender):
    mqtt_sender.send_message('Forward_Time_Inches', [str(speed), str(inches)])
    print('Forward_Time_Inches', speed, inches)
def handle_forward_inches_button(speed,inches,mqtt_sender):
    mqtt_sender.send_message('Forward_Inches', [str(speed), str(inches)])
    print('Forward_Inches', speed, inches)



def get_Sprint_1_Beeper_System_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Sound System")
    number_of_beeps_label = ttk.Label(frame, text="Number of Beeps")
    tone_duration_label = ttk.Label(frame, text="Duration of Tone")
    tone_frequency_label = ttk.Label(frame, text="Tone Frequency")
    speak_text_label = ttk.Label(frame, text="Text to Speech")

    number_of_beeps= ttk.Entry(frame, width=8)
    number_of_beeps.insert(0, "10")
    tone_duration = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    tone_duration.insert(0, "10")
    tone_frequency = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    tone_frequency.insert(0, "10")
    speak_text = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    speak_text.insert(0, "Type Here")


    beep_button = ttk.Button(frame, text="Play Beeps")
    tone_button = ttk.Button(frame, text="Play Tone")
    speak_button = ttk.Button(frame, text="Read Text")


    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    number_of_beeps_label.grid(row=1, column=0)
    tone_duration_label.grid(row=1, column=1)
    tone_frequency_label.grid(row=1, column=2)
    speak_text_label.grid(row=1, column=3)

    number_of_beeps.grid(row=2, column=0)
    tone_duration.grid(row=2, column=1)
    tone_frequency.grid(row=2, column=2)
    speak_text.grid(row=2, column=3)

    beep_button.grid(row=3, column=0)
    tone_button.grid(row=3, column=1)
    speak_button.grid(row=3, column=3)

    # Set the button callbacks:
    beep_button["command"] = lambda: handle_beep_button(number_of_beeps.get(), mqtt_sender)
    tone_button["command"] = lambda: handle_tone_button(tone_duration.get(), tone_frequency.get(), mqtt_sender)
    speak_button["command"] = lambda: handle_speak_button(speak_text.get(), mqtt_sender)
    return frame


def handle_beep_button(numberofbeeps,mqtt_sender):
    mqtt_sender.send_message('beep_button', [str(numberofbeeps)])
    print('beep_button',numberofbeeps)
def handle_tone_button(duration,frequency,mqtt_sender):
    mqtt_sender.send_message('tone_button', [str(duration), str(frequency)])
    print('tone_button', duration, frequency)
def handle_speak_button(text,mqtt_sender):
    mqtt_sender.send_message('speak_button', [text])
    print('speak_button', text)


def get_Katana_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Katana's System")
    obtain_with_sensor_label = ttk.Label(frame, text="Pick Up Object")
    obtain_with_sensor_button = ttk.Button(frame, text="Get")

    rate_of_frequency_label = ttk.Label(frame, text="Frequency Rate (Increasing)")
    rate_of_frequency = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    rate_of_frequency.insert(0, "10")
    initial_frequency_label = ttk.Label(frame, text="Initial Frequency")
    initial_frequency = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    initial_frequency.insert(0, "5")

    obtain_with_camera_label = ttk.Label(frame, text="Pick up Object with Camera")
    obtain_with_camera_button = ttk.Button(frame, text="Get")

    spin_speed_label = ttk.Label(frame, text="Spinning Speed")
    spin_speed = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    spin_speed.insert(0, "10")
    spin_direction_label = ttk.Label(frame, text="Spinning Direction")
    spin_direction = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    spin_direction.insert(0, "Counter Clockwise")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    obtain_with_sensor_label.grid(row=1, column=0)
    obtain_with_sensor_button.grid(row=1, column=1)
    rate_of_frequency.grid(row=2, column=0)
    rate_of_frequency.grid(row=2, column=1)
    initial_frequency.grid(row=3, column=0)
    initial_frequency.grid(row=3, column=1)

    obtain_with_camera_label.grid(row=4, column=0)
    obtain_with_camera_button.grid(row=4, column=1)
    spin_speed_label.grid(row=5, column=0)
    spin_speed.grid(row=5, column=1)
    spin_direction.grid(row=6, column=0)
    spin_direction.grid(row=6, column=1)

    # Set the button callbacks:
    #obtain_with_sensor_button["command"] = lambda: handle_obtain_with_sensor_button(rate_of_frequency.get(),
    #                                                                                initial_frequency.get(),
    #                                                                                mqtt_sender)

    #obtain_with_camera_button["command"] = lambda: handle_obtain_with_camera_button(spin_speed.get(),
    #                                                                                spin_direction.get(),
    #                                                                                rate_of_frequency.get(),
    #                                                                                initial_frequency.get(),
    #                                                                                mqtt_sender)
    return frame


def get_Nick_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Nick's Sprint 2 System")
    proximity_label = ttk.Label(frame, text="Go to and Pick up Object (Proximity)")
    proximity_button = ttk.Button(frame, text="Run Proximity Grab")

    camera_label = ttk.Label(frame, text="Go to and Pick up Object (Camera)")
    camera_button = ttk.Button(frame, text="Run Camera Grab")

    line_follower_label = ttk.Label(frame, text="Line Follower (Bang Bang Method)")
    line_button = ttk.Button(frame, text="Follow Line")

    rate_of_beeps_label = ttk.Label(frame, text="Beep Rate Increase")
    rate_of_beeps= ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    rate_of_beeps.insert(0, "10")
    initial_beeps_label = ttk.Label(frame, text="Initial Beep Rate")
    initial_beeps = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    initial_beeps.insert(0, "5")

    speed_label = ttk.Label(frame, text="Turning Speed")
    speed = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    speed.insert(0, "100")
    direction_label = ttk.Label(frame, text="Turning Direction, Clockwise or Counter-Clockwise")
    direction = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    direction.insert(0, "Clockwise")

    starting_side_label = ttk.Label(frame, text="Turning Direction, Right or Left")
    starting_side = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    starting_side.insert(0, "Right")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    proximity_label.grid(row=1, column=0)
    proximity_button.grid(row=1, column=1)
    rate_of_beeps_label.grid(row=2, column=0)
    rate_of_beeps.grid(row=2, column=1)
    initial_beeps_label.grid(row=3, column=0)
    initial_beeps.grid(row=3, column=1)

    camera_label.grid(row=4, column=0)
    camera_button.grid(row=4, column=1)
    speed_label.grid(row=5, column=0)
    speed.grid(row=5, column=1)
    direction_label.grid(row=6, column=0)
    direction.grid(row=6, column=1)

    line_follower_label.grid(row=7, column=0)
    line_button.grid(row=7, column=1)
    starting_side_label.grid(row=8, column=0)
    starting_side.grid(row=8, column=1)

    # Set the button callbacks:
    proximity_button["command"] = lambda: handle_proximity_button(rate_of_beeps.get(), initial_beeps.get(), mqtt_sender)
    camera_button["command"] = lambda: handle_camera_button(speed.get(),direction.get(),rate_of_beeps.get(), initial_beeps.get(), mqtt_sender)
    line_button["command"] = lambda: handle_line_button(starting_side.get(), mqtt_sender)
    return frame

def handle_proximity_button(rate_of_beeps, initial_beeps, mqtt_sender):
    mqtt_sender.send_message('m1proximity_button', [str(rate_of_beeps),str(initial_beeps)])
    print('proximity',rate_of_beeps, initial_beeps)
def handle_camera_button(speed,direction,rate_of_beeps, initial_beeps, mqtt_sender):
    mqtt_sender.send_message('m1camera_button', [str(speed), str(direction),str(rate_of_beeps),str(initial_beeps)])
    print('camera', speed, direction, rate_of_beeps, initial_beeps)
def handle_line_button(starting_side, mqtt_sender):
    mqtt_sender.send_message('m1line_button', [str(starting_side)])
    print('line', starting_side)

##COLOR FRAMING
def get_Sprint_2_Color_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
      :type  window:       ttk.Frame | ttk.Toplevel
      :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()

    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Color Sensor")
    intensity_less_label = ttk.Label(frame, text="Go Until Intensity is Less Than")
    intensity_less_button = ttk.Button(frame, text="Run Less than Intensity")

    intensity_greater_label = ttk.Label(frame, text="Go Until Intensity is Greater Than")
    intensity_greater_button = ttk.Button(frame, text="Run Greater than Intensity")

    until_color_label = ttk.Label(frame, text="Go Until Color")
    until_color_button = ttk.Button(frame, text="Run Go Until Color")

    until_not_color_label = ttk.Label(frame, text="Go Until Not Color")
    until_not_color_button = ttk.Button(frame, text="Run Go Until Not Color")

    color_label = ttk.Label(frame, text="Color")
    color= ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    color.insert(0, "Red")
    speed_label = ttk.Label(frame, text="Speed")
    speed = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    speed.insert(0, "100")

    intensity_label = ttk.Label(frame, text="Light Intensity")
    intensity = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    intensity.insert(0, "50")



    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    color_label.grid(row=1, column=0)
    color.grid(row=2, column=0)
    speed_label.grid(row=1, column=1)
    speed.grid(row=2, column=1)
    intensity_label.grid(row=1, column=2)
    intensity.grid(row=2, column=2)

    intensity_less_label.grid(row=3, column=0)
    intensity_less_button.grid(row=4, column=0)
    intensity_greater_label.grid(row=5, column=0)
    intensity_greater_button.grid(row=6, column=0)

    until_color_label.grid(row=3, column=2)
    until_color_button.grid(row=4, column=2)
    until_not_color_label.grid(row=5, column=2)
    until_not_color_button.grid(row=6, column=2)


    # Set the button callbacks:
    intensity_less_button["command"] = lambda: handle_intensity_less_button(speed.get(), intensity.get(), mqtt_sender)
    intensity_greater_button["command"] = lambda: handle_intensity_greater_button(speed.get(),intensity.get(), mqtt_sender)
    until_color_button["command"] = lambda: handle_until_color_button(speed.get(),color.get(), mqtt_sender)
    until_not_color_button["command"] = lambda: handle_until_not_color_button(speed.get(),color.get(), mqtt_sender)
    return frame

def handle_intensity_less_button(speed, intensity, mqtt_sender):
    mqtt_sender.send_message('intensity_less_button', [str(speed),str(intensity)])
    print('intensity_less_button',speed, intensity)

def handle_intensity_greater_button(speed, intensity, mqtt_sender):
    mqtt_sender.send_message('intensity_greater_button', [str(speed), str(intensity)])
    print('intensity_greater_button', speed, intensity)

def handle_until_color_button(speed,color, mqtt_sender):
    mqtt_sender.send_message('until_color_button', [str(speed),str(color)])
    print('until_color_button', speed,color)

def handle_until_not_color_button(speed,color, mqtt_sender):
    mqtt_sender.send_message('until_not_color_button', [str(speed),str(color)])
    print('until_not_color_button', speed,color)



##PROXIMITY SENSOR
def get_Sprint_2_Proximity_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
        :type  window:       ttk.Frame | ttk.Toplevel
        :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Proximity Sensor")

    distance_less_label = ttk.Label(frame, text="Go Until Distance is Less Than")
    distance_less_button = ttk.Button(frame, text="Run Less than Distance")

    distance_greater_label = ttk.Label(frame, text="Go Until Distance is Greater Than")
    distance_greater_button = ttk.Button(frame, text="Run Greater than Distance")

    until_distance_label = ttk.Label(frame, text="Go Until Distance Within")
    until_distance_button = ttk.Button(frame, text="Run Go Until Distance Within")



    inches_label = ttk.Label(frame, text="Inches")
    inches = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    inches.insert(0, "10")

    speed_label = ttk.Label(frame, text="Speed")
    speed = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    speed.insert(0, "100")

    delta_label = ttk.Label(frame, text="Delta Distance")
    delta = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    delta.insert(0, "50")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)

    distance_less_label.grid(row=3, column=0)
    distance_less_button.grid(row=4, column=0)
    distance_greater_label.grid(row=3, column=1)
    distance_greater_button.grid(row=4, column=1)
    until_distance_label.grid(row=3, column=2)
    until_distance_button.grid(row=4, column=2)

    delta_label.grid(row=1, column=0)
    delta.grid(row=2, column=0)

    speed_label.grid(row=1, column=1)
    speed.grid(row=2, column=1)

    inches_label.grid(row=1, column=2)
    inches.grid(row=2, column=2)

    # Set the button callbacks:
    distance_greater_button["command"] = lambda: handle_distance_greater_button(speed.get(), inches.get(), mqtt_sender)
    distance_less_button["command"] = lambda: handle_distance_less_button(speed.get(), inches.get(),mqtt_sender)
    until_distance_button["command"] = lambda: handle_until_distance_button(speed.get(), inches.get(), delta.get(), mqtt_sender)
    return frame


def handle_distance_greater_button(speed, inches, mqtt_sender):
    mqtt_sender.send_message('distance_greater_button', [str(speed), str(inches)])
    print('distance_greater_button', speed, inches)
def handle_distance_less_button(speed, inches,mqtt_sender):
    mqtt_sender.send_message('distance_less_button', [str(speed), str(inches)])
    print('distance_less_button', speed, inches)
def handle_until_distance_button(speed, inches, delta, mqtt_sender):
    mqtt_sender.send_message('until_distance_button', [str(speed), str(inches),str(delta)])
    print('until_distance_button', speed, inches, delta)




##PROXIMITY SENSOR
def get_Sprint_2_Camera_frame(window, mqtt_sender):
    """
    Constructs and returns a frame on the given window, where the frame
    has Beeper objects that control the EV3 robot's motion
    by passing messages using the given MQTT Sender.
        :type  window:       ttk.Frame | ttk.Toplevel
        :type  mqtt_sender:  com.MqttClient
    """
    # Construct the frame to return:
    frame = ttk.Frame(window, padding=10, borderwidth=5, relief="ridge")
    frame.grid()
    # Construct the widgets on the frame:
    frame_label = ttk.Label(frame, text="Camera Sensor")

    counter_clockwise_label = ttk.Label(frame, text="Search Counterclockwise")
    counter_clockwise_button = ttk.Button(frame, text="Run CCW Search")

    clockwise_label = ttk.Label(frame, text="Search Counterclockwise")
    clockwise_button = ttk.Button(frame, text="Run CW Search")

    speed_label = ttk.Label(frame, text="Speed")
    speed = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    speed.insert(0, "100")

    area_label = ttk.Label(frame, text="Area Size")
    area = ttk.Entry(frame, width=8, justify=tkinter.LEFT)
    area.insert(0, "20")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)

    counter_clockwise_label.grid(row=1, column=0)
    counter_clockwise_button.grid(row=2, column=0)
    clockwise_label.grid(row=1, column=2)
    clockwise_button.grid(row=2, column=2)


    area_label.grid(row=1, column=1)
    area.grid(row=2, column=1)

    speed_label.grid(row=3, column=1)
    speed.grid(row=4, column=1)

    # Set the button callbacks:
    counter_clockwise_button["command"] = lambda: handle_counter_clockwise_button(speed.get(), area.get(), mqtt_sender)
    clockwise_button["command"] = lambda: handle_clockwise_button(speed.get(), area.get(),mqtt_sender)

    return frame

def handle_counter_clockwise_button(speed, area, mqtt_sender):
    mqtt_sender.send_message('camera_counter_clockwise_button', [str(speed), str(area)])
    print('camera_counter_clockwise_button', speed, area)

def handle_clockwise_button(speed, area, mqtt_sender):
    mqtt_sender.send_message('camera_clockwise_button', [str(speed), str(area)])
    print('camera_clockwise_button', speed, area)
