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

    delegate = PcDelegate()
    sender = com.MqttClient(delegate)
    sender.connect_to_ev3()
    time.sleep(0.1)

    # -------------------------------------------------------------------------
    # The root TK object for the GUI:
    # -------------------------------------------------------------------------

    root = tkinter.Tk()
    root.title('M3 Run on Laptop')
    root.grid_columnconfigure(0, weight=1)
    root.attributes('-fullscreen', True)

    # -------------------------------------------------------------------------
    # The main frame, upon which the other frames are placed.
    # -------------------------------------------------------------------------

    main_frame = tkinter.Frame(root, borderwidth=5, relief='groove')
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid(sticky="EWNS")
    # -------------------------------------------------------------------------
    # Sub-frames for the shared GUI that the team developed:
    # -------------------------------------------------------------------------

    teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper = get_shared_frames(main_frame, sender)

    # -------------------------------------------------------------------------
    # Frames that are particular to my individual contributions to the project.
    # -------------------------------------------------------------------------
    # Done: Implement and call get_my_frames(...)

    feature_9 = feature_9_frame(main_frame, sender)
    feature_10 = feature_10_frame(main_frame, sender)
    sprint_3_graph, graph = sprint_3_graph_frame(main_frame)
    sprint_3_frame = sprint_3_others(main_frame, sender)

    # -------------------------------------------------------------------------
    # Grid the frames.
    # -------------------------------------------------------------------------

    grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper)
    grid_my_frames(feature_9, feature_10, sprint_3_graph, sprint_3_frame)

    # -------------------------------------------------------------------------
    # Other Setup
    # -------------------------------------------------------------------------
    delegate.set_graph(graph)
    root.update_idletasks()
    root.update()
    graph.update_graph_size(sprint_3_graph)
    graph.setup()

    # -------------------------------------------------------------------------
    # The event loop:
    # -------------------------------------------------------------------------


    while True:
        if delegate.end == 1:
            for i in delegate.point_list:
                graph.draw_graph(i)
            print(delegate.point_list)
            delegate.end = 0
        root.update_idletasks()
        root.update()


def get_shared_frames(main_frame, mqtt_sender):
    teleop_frame = shared_gui.get_teleoperation_frame(main_frame, mqtt_sender)
    arm_frame = shared_gui.get_arm_frame(main_frame, mqtt_sender)
    control_frame = shared_gui.get_control_frame(main_frame, mqtt_sender)
    sprint_1_drive_system = shared_gui.get_Sprint_1_Drive_System_frame(main_frame, mqtt_sender)
    sprint_1_beeper = shared_gui.get_Sprint_1_Beeper_System_frame(main_frame, mqtt_sender)

    return teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper


def grid_frames(teleop_frame, arm_frame, control_frame, sprint_1_drive_system, sprint_1_beeper):
    teleop_frame.grid(row=0, column=0, sticky="EW")
    arm_frame.grid(row=1, column=0, sticky="EW")
    sprint_1_drive_system.grid(row=2, column=0, sticky="EW")
    sprint_1_beeper.grid(row=3, column=0, sticky="EW")
    control_frame.grid(row=4, column=0, sticky="EW")


def grid_my_frames(feature_9, feature_10, sprint_3_graph, sprint_3_frame):
    feature_9.grid(row=5, column=0, sticky="EW")
    feature_10.grid(row=6, column=0, sticky="EW")
    sprint_3_graph.grid(row=0, column=1, rowspan=7, sticky="EWNS")
    sprint_3_frame.grid(row=7, column=0, sticky="EW")

# -------------------------------------------------------------------------
# Feature 10
# -------------------------------------------------------------------------


def feature_10_frame(frame, sender):
    feature_frame = ttk.Frame(frame, padding=10, borderwidth=5, relief="ridge")
    feature_10_widgets(feature_frame, sender)

    return feature_frame


def feature_10_widgets(frame, sender):
    # -----------------------------------------------------------------------------
    # Setup
    # -----------------------------------------------------------------------------
    speed_label = ttk.Label(frame, text="Speed")
    direction_label = ttk.Label(frame, text="Spin Direction (unchecked is cw)")
    title_label = ttk.Label(frame, text="Feature 10")

    speed_entry = ttk.Entry(frame)
    direction_checkbox = ttk.Checkbutton(frame)

    feature_10_button = ttk.Button(frame, text="Feature 10")
    feature_10_button["command"] = lambda: sender.send_message("m3_feature_10", [speed_entry.get(),
                                                                                 direction_checkbox.state()])
    # -----------------------------------------------------------------------------
    # Grid
    # -----------------------------------------------------------------------------
    speed_label.grid(row=1, column=0)
    direction_label.grid(row=2, column=0)
    title_label.grid(row=0, column=0)

    speed_entry.grid(row=1, column=1)
    direction_checkbox.grid(row=2, column=1)

    feature_10_button.grid(row=0, column=1)

# -------------------------------------------------------------------------
# Feature 9
# -------------------------------------------------------------------------


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

# -------------------------------------------------------------------------
# Sprint 3
# -------------------------------------------------------------------------


class PcDelegate(object):
    def __init__(self):
        self.graph = None
        self.end = 0
        self.point_list = []

    def set_graph(self, graph):
        self.graph = graph

    def draw_graph(self, point):
        self.end = 1
        self.point_list = point

    def print_message(self, message):
        print(message)


class Graph(object):
    def __init__(self, canvas):
        self.canvas = canvas
        self.last_point = (50, 350)

    def setup(self):
        self.canvas.create_text(20, 770, text='Time')
        self.canvas.create_text(20, 20, text='Output')
        for x in range(50, 1150, 100):
            self.canvas.create_text(x, 770, text=str((x - 50) // 2))
        self.canvas.create_line(50, 760, 1050, 760)
        self.canvas.create_line(50, 760, 50, 0)
        for y in range(50, 680, 30):
            self.canvas.create_text(30, y, text=str(int(100 - ((y - 50) / 3))))
        #tkinter.Canvas.

    def update_graph_size(self, frame):
        # final size is about 1000 x 750
        self.canvas.config(width=frame.winfo_width(), height=frame.winfo_height())

    def draw_graph(self, point):
        print('point', point)
        print('last point', self.last_point)
        self.canvas.create_line(self.last_point[0], self.last_point[1], point[0], point[1])
        self.last_point = point


def sprint_3_graph_frame(frame):
    canvas_frame = ttk.Frame(frame)
    graph = Graph(tkinter.Canvas(canvas_frame, width=100, height=100))

    graph.canvas.grid()

    return canvas_frame, graph


def sprint_3_others(frame, sender):
    others_frame = ttk.Frame(frame)
    button = ttk.Button(others_frame, text='Sprint 3', width=100)
    button['command'] = lambda: sender.send_message('m3_sprint_3', [])
    button.grid(sticky='EWNS')

    return others_frame

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
