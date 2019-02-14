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

    feature_9 = feature_9_frame(main_frame, sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------

    grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper, feature_9)

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


def grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper, feature_9):
    teleop_frame.grid(row=0, column=0)
    arm_frame.grid(row=1, column=0)
    sprint_1_drive_system.grid(row=2, column=0)
    sprint_1_beeper.grid(row=3, column=0)
    control_frame.grid(row=4, column=0)
    feature_9.grid(row=5, column=0)



def feature_9_frame(frame, sender):
    feature_frame = ttk.Frame(frame, padding=10, borderwidth=5, relief="ridge")
    feature_9_widgets(feature_frame, sender)

    return feature_frame


def feature_9_widgets(frame, sender):
    # -----------------------------------------------------------------------------
    # Setup
    # -----------------------------------------------------------------------------
    init_rate_label = ttk.Label(frame, text="Initial Cycle Rate (cycles/sec)")
    acceleration_label = ttk.Label(frame, text="Acceleration (cycles/sec/inch)")
    title_label = ttk.Label(frame, text="Feature 9")

    init_rate_entry = ttk.Entry(frame)
    acceleration_entry = ttk.Entry(frame)

    feature_9_button = ttk.Button(frame, text="Feature 9")
    feature_9_button["command"] = lambda: sender.send_message("m3_feature_9", [init_rate_entry.get(),
                                                                               acceleration_entry.get()])
    # -----------------------------------------------------------------------------
    # Grid
    # -----------------------------------------------------------------------------
    init_rate_label.grid(row=1, column=0)
    acceleration_label.grid(row=2, column=0)
    title_label.grid(row=0, column=0)

    init_rate_entry.grid(row=1, column=1)
    acceleration_entry.grid(row=2, column=1)

    feature_9_button.grid(row=0, column=1)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
