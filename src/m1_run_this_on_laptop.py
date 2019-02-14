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
import m1_personal_GUI
import time
import m1_personal_delegate

def main():
    """
    This code, which must run on a LAPTOP:
      1. Constructs a GUI for my part of the Capstone Project.
      2. Communicates via MQTT with the code that runs on the EV3 robot.
    """
    # -------------------------------------------------------------------------
    # Construct and connect the MQTT Client:
    # -------------------------------------------------------------------------
    delegate = m1_personal_delegate.ROBOT_DelegateThatReceives
    mqtt_sender = com.MqttClient(delegate)
    mqtt_sender.connect_to_ev3()

    time.sleep(1)  # Time to allow the MQTT setup.
    print()

    #Inital Position of Robot
    previous_click = [250, 250]
    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------
    root = tkinter.Tk()
    root.title("MQTT EV3 Remote")

    canvasbase = tkinter.Tk()
    canvasbase.title("Drawing Frame")



    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------
    main_frame = ttk.Frame(root, padding=10, borderwidth=5,relief='groove')
    main_frame.grid()














    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------
    arm_frame,control_frame,teleoperation_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Nick_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame=get_shared_frames(main_frame,mqtt_sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    drawpad = tkinter.Canvas(canvasbase, width=500, height=500)
    drawpad.configure(bg="white")
    drawpad.pack()
    buttonBG = drawpad.create_rectangle(0, 0, 100, 30, fill="grey40", outline="grey60")
    buttonTXT = drawpad.create_text(50, 15, text="Click to Run")

    #Functions Triggered:
    def click(event):
        x= event.x
        y= event.y
        print("Clicked")
        print('{}, {}'.format(x, y))
        drawpad.create_line(previous_click[len(previous_click)-2], previous_click[len(previous_click)-1], x, y)
        previous_click.append(x)
        previous_click.append(y)
        mqtt_sender.send_message('Store_Path',[x,y])

    def clicked(event):
        for k in range(len(previous_click)):
            print(previous_click[k],end=' ')
        mqtt_sender.send_message('Follow_Path')



    # Get The Clicks
    drawpad.tag_bind(buttonBG, "<Button-1>", clicked)
    drawpad.tag_bind(buttonTXT, "<Button-1>", clicked)
    canvasbase.bind('<Button>', click)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------
    grid_frames(teleoperation_frame,arm_frame,control_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Nick_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame)
    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------
    root.mainloop()


def get_shared_frames(main_frame, mqtt_sender):
    arm_frame=m1_personal_GUI.get_arm_frame(main_frame,mqtt_sender)
    control_frame=m1_personal_GUI.get_control_frame(main_frame,mqtt_sender)
    teleoperation_frame=m1_personal_GUI.get_teleoperation_frame(main_frame,mqtt_sender)
    Sprint_1_Drive_System_frame=m1_personal_GUI.get_Sprint_1_Drive_System_frame(main_frame,mqtt_sender)
    Sprint_1_Beeper_System_frame=m1_personal_GUI.get_Sprint_1_Beeper_System_frame(main_frame,mqtt_sender)
    Nick_frame=m1_personal_GUI.get_Nick_frame(main_frame,mqtt_sender)
    Sprint_2_Color_frame=m1_personal_GUI.get_Sprint_2_Color_frame(main_frame,mqtt_sender)
    Sprint_2_Proximity_frame=m1_personal_GUI.get_Sprint_2_Proximity_frame(main_frame,mqtt_sender)
    Sprint_2_Camera_frame=m1_personal_GUI.get_Sprint_2_Camera_frame(main_frame,mqtt_sender)
    return  arm_frame,control_frame,teleoperation_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Nick_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame

def grid_frames(teleop_frame, arm_frame, control_frame,Sprint_1_Drive_System_frame,Sprint_1_Beeper_System_frame,Nick_frame,Sprint_2_Color_frame,Sprint_2_Proximity_frame,Sprint_2_Camera_frame):
    teleop_frame.grid(row=0,column=0)
    arm_frame.grid(row=1,column=0)
    control_frame.grid(row=2,column=0)
    Sprint_1_Drive_System_frame.grid(row=0,column=1)
    Sprint_1_Beeper_System_frame.grid(row=1,column=1)
    Nick_frame.grid(row=2,column=1)
    Sprint_2_Color_frame.grid(row=0,column=2)
    Sprint_2_Proximity_frame.grid(row=1,column=2)
    Sprint_2_Camera_frame.grid(row=2,column=2)


# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()