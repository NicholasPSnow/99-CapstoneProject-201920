"""
  Capstone Project.  Code to run on a LAPTOP (NOT the robot).
  Displays the Graphical User Interface (GUI) and communicates with the robot.

  Authors:  Your professors (for the framework)
    and Nicholas Snow.
  Winter term, 2018-2019.
"""

import mqtt_remote_method_calls as com
import tkinter
from tkinter import ttk
import shared_gui
import time


def get_left(left_speed_entry):
    contents_of_entry_box = left_speed_entry.get()
    return contents_of_entry_box
def get_right(right_speed_entry):
    contents_of_entry_box = right_speed_entry.get()
    return contents_of_entry_box

def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    name1 = input("Enter one name (subscriber): ")
    name2 = input("Enter another name (publisher): ")
    mqtt_client = com.MqttClient()
    mqtt_client.connect(name1, name2)
    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("MQTT Remote")

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=20)
    main_frame.grid()

    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    # Entry Box
    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=1)
    left_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.LEFT)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=1)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=3)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=3)



    # Buttons:
    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=2)
    forward_button['command'] = lambda: mqtt_client.send_message("Forward", [get_left(left_speed_entry),
                                                                             get_right(right_speed_entry)])
    root.bind('<Up>', lambda event: print("Forward key"))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=1)
    left_button['command'] = lambda: mqtt_client.send_message("Left")
    root.bind('<Left>', lambda event: print("Left key"))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    stop_button['command'] = lambda: mqtt_client.send_message("Stop")
    root.bind('<space>', lambda event: print("Stop key"))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=3)
    right_button['command'] = lambda: mqtt_client.send_message("Right")
    root.bind('<Right>', lambda event: print("Right key"))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=2)
    back_button['command'] = lambda: mqtt_client.send_message("Backward", [get_left(left_speed_entry),
                                                                           get_right(right_speed_entry)])
    root.bind('<Down>', lambda event: print("Back key"))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=1)
    up_button['command'] = lambda: mqtt_client.send_message("Arm_Up")
    root.bind('<u>', lambda event: print("Up key"))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=1)
    down_button['command'] = lambda: mqtt_client.send_message("Arm_Down")
    root.bind('<j>', lambda event: print("Down key"))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=3)
    q_button['command'] = lambda: mqtt_client.send_message("Quit")
    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=3)
    e_button['command'] = lambda: exit()

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # TODO: Implement and call get_my_frames(...)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------


    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    pass


def grid_frames(teleop_frame, arm_frame, control_frame):
    pass


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()