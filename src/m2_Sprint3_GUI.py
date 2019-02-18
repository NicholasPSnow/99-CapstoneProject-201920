"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Katana Colledge.
  Winter term, 2018-2019.
"""

import tkinter
from tkinter import ttk
import time
from tkinter import messagebox

def main_frame(window, mqtt_sender):
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

    main_frame_label = ttk.Label(frame, text="SS-294 Communication Window")

    establish_link_label = ttk.Label(frame, text="Establish Link")
    establish_link_button = ttk.Button(frame, text="Connect")

    status_label = ttk.Label(frame, text="Report Status")
    status_button = ttk.Label(frame, text="Status")



    # Grid the widgets:
    main_frame_label.grid(row=0, column=2)
    establish_link_label.grid(row=1, column=1)
    establish_link_button.grid(row=2, column=1)
    status_label.grid(row=1,column=3)
    status_button.grid(row=2,column = 3)

    # Set the button callbacks:
    establish_link_button["command"] = lambda: handle_establish_link_button(mqtt_sender)
    status_button["command"] = lambda: handle_status_button(mqtt_sender)

    # Handlers
    def handle_establish_link_button(mqtt_sender):
        print('handler')
        mqtt_sender.send_message('establish_link_button')
        print('Established link')
    def handle_status_button(mqtt_sender):
        print('handler')
        mqtt_sender.send_message('establish_status_button')
        print('Obtaining Status')








