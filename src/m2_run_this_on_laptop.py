"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Katana Colledge.
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

    mqtt_sender = com.MqttClient()
    mqtt_sender.connect_to_ev3()

    # -------------------------------------------------------------------------
    # The root Tk object for the GUI:
    # -------------------------------------------------------------------------
    root=tkinter.Tk()
    root.title("CSSE 120 Final Project, Katana Colledge, Winter 2018-19")


    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------

    main_frame = ttk.Frame(root,padding = 20, borderwidth = 3, relief="groove")
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------

    arm_frame,control_frame,teleoperation_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Katana_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame=get_shared_frames(main_frame,mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # ---------------------------------------------------------------- ---------

    grid_frames(teleoperation_frame,arm_frame,control_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Katana_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame)

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    arm_frame=shared_gui.get_arm_frame(main_frame,mqtt_sender)
    control_frame=shared_gui.get_control_frame(main_frame,mqtt_sender)
    teleoperation_frame=shared_gui.get_teleoperation_frame(main_frame,mqtt_sender)
    Sprint_1_Drive_System_frame=shared_gui.get_Sprint_1_Drive_System_frame(main_frame,mqtt_sender)
    Sprint_1_Beeper_System_frame=shared_gui.get_Sprint_1_Beeper_System_frame(main_frame,mqtt_sender)
    Katana_frame=shared_gui.get_Katana_frame(main_frame,mqtt_sender)
    Sprint_2_Color_frame=shared_gui.get_Sprint_2_Color_frame(main_frame,mqtt_sender)
    Sprint_2_Proximity_frame=shared_gui.get_Sprint_2_Proximity_frame(main_frame,mqtt_sender)
    Sprint_2_Camera_frame=shared_gui.get_Sprint_2_Camera_frame(main_frame,mqtt_sender)
    return  arm_frame,control_frame,teleoperation_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Katana_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame

def grid_frames(teleop_frame, arm_frame, control_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Katana_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame):
    teleop_frame.grid(row=0,column=0)
    arm_frame.grid(row=1,column=0)
    control_frame.grid(row=2,column=0)
    Sprint_1_Drive_System_frame.grid(row=0,column=1)
    Sprint_1_Beeper_System_frame.grid(row=1,column=1)
    Katana_frame.grid(row=2,column=1)
    Sprint_2_Color_frame.grid(row=0,column=2)
    Sprint_2_Proximity_frame.grid(row=1,column=2)
    Sprint_2_Camera_frame.grid(row=2,column=2)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()