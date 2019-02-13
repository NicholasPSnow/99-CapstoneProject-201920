"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Zach Kelly.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui
import time


def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------

    sender = com.MqttClient()
    sender.connect_to_ev3()
    time.sleep(0.1)

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------

    root = tkinter.Tk()
    root.title('M3 Run on Laptop')

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------

    main_frame = tkinter.Frame(root, borderwidth=5, relief='groove')
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------

    teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper = get_shared_frames(main_frame, sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    feature_11_frame = get_my_frames(main_frame)
    feature_11_frame.grid(row=5, column=0)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------

    grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------

    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    sprint_1_drive_system = shared_gui.get_Sprint_1_Drive_System_frame(main_frame, mqtt_sender)
    sprint_1_beeper = shared_gui.get_Sprint_1_Beeper_System_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper


def grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    sprint_1_drive_system.grid(row=2, column=0)
    sprint_1_beeper.grid(row=3, column=0)
    control_frame.grid(row=4, column=0)

def get_my_frames(frame, mqtt_sender):
    feature_11_frame = ttk.Frame(frame, padding=10, borderwidth=5, relief="ridge")

    b_label = ttk.Label(feature_11_frame, text="B Value")
    b_entry = ttk.Entry(feature_11_frame)
    k1_label = ttk.Label(feature_11_frame, text="K1 Value")
    k1_entry = ttk.Entry(feature_11_frame)
    kd1_label = ttk.Label(feature_11_frame, text="KD1 Value")
    kd1_entry = ttk.Entry(feature_11_frame)
    kd2_label = ttk.Label(feature_11_frame, text="KD2 Value")
    kd2_entry = ttk.Entry(feature_11_frame)
    button = ttk.Button(feature_11_frame, text='Run Feature 11')
    title = ttk.Label(feature_11_frame, text='Feature 11')

    b_label.grid(row=2, column=0)
    b_entry.grid(row=3, column=0)
    k1_label.grid(row=2, column=2)
    k1_entry.grid(row=3, column=2)
    kd1_label.grid(row=4, column=0)
    kd1_entry.grid(row=5, column=0)
    kd2_label.grid(row=4, column=2)
    kd2_entry.grid(row=5, column=2)
    button.grid(row=1, column=1)
    title.grid(row=0, column=1)

    button['command'] = lambda: handle_feature_11(mqtt_sender, b_entry.get(), k1_entry.get(), kd1_entry.get(), kd2_entry.get())

    return feature_11_frame


def handle_feature_11(mqtt_sender, b, k1, kd1, kd2):
    mqtt_sender.send_message("feature_11", [b, k1, kd1, kd2])

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()
