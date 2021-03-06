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
        if delegate.end == 1:  # this detects that the robot has finished following the line
            graph.setup()
            for i in delegate.point_list:
                # this scales and draws the points sent by the robot for the graph
                graph.draw_graph((50 + (i[0] - delegate.point_list[0][0]) * 10, 350 + 12 * i[1]))
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
    """
    creates a frame with all of the gui parts for feature 10
    :param frame: the master frame
    :param sender: the mqtt client used by the buttons to send commands
    """
    feature_frame = ttk.Frame(frame, padding=10, borderwidth=5, relief="ridge")
    feature_10_widgets(feature_frame, sender)

    return feature_frame


def feature_10_widgets(frame, sender):
    """
    creates and places all of the widgets for feature 10
    :param frame: the master frame
    :param sender: the mqtt client used by the buttons to send commands
    """
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
    """
    creates a frame with all of the gui parts for feature 9
    :param frame: the master frame
    :param sender: the mqtt client used by the buttons to send commands
    """
    feature_frame = ttk.Frame(frame, padding=10, borderwidth=5, relief="ridge")
    feature_9_widgets(feature_frame, sender)

    return feature_frame


def feature_9_widgets(frame, sender):
    """
    creates and places all of the widgets for feature 9
    :param frame: the master frame
    :param sender: the mqtt client used by the buttons to send commands
    """
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
    """
    handles commands sent to the pc by the robot
    """
    def __init__(self):
        self.graph = None
        self.end = 0
        self.point_list = []

    def set_graph(self, graph):
        self.graph = graph

    def graph_data(self, point):
        self.point_list.append(point)

    def draw_graph(self):
        self.end = 1


class Graph(object):
    """
    used to manipulate the canvas
    """
    def __init__(self, canvas):
        self.canvas = canvas
        self.last_point = (50, 350)

    def setup(self):
        """
        clears the canvas then draws the x-axis and y-axis
        """
        self.canvas.delete('all')
        self.canvas.create_text(20, 770, text='Time')
        self.canvas.create_text(20, 20, text='Delta')
        for x in range(50, 1150, 100):
            self.canvas.create_text(x, 770, text=str((x - 50) / 20))
        self.canvas.create_line(50, 760, 1050, 760)
        self.canvas.create_line(50, 760, 50, 0)
        for y in range(50, 680, 30):
            self.canvas.create_text(30, y, text=str(float(25 - ((y - 50) / 12))))

    def update_graph_size(self, frame):
        """
        maximizes the size of the graph to fill all remaining space
        final size is about 1000 x 750 pixels
        :param frame: the master frame
        """
        self.canvas.config(width=frame.winfo_width(), height=frame.winfo_height())

    def draw_graph(self, point):
        """
        draws a line from the last point plotted to a new point
        :param point: a point on the xy plane in the form of tuple
        :return:
        """
        print('point', point)
        print('last point', self.last_point)
        self.canvas.create_line(self.last_point[0], self.last_point[1], point[0], point[1])
        self.last_point = point


def sprint_3_graph_frame(frame):
    """
    creates and returns the canvas and its frame
    :param frame: the master frame
    """
    canvas_frame = ttk.Frame(frame)
    graph = Graph(tkinter.Canvas(canvas_frame, width=100, height=100))

    graph.canvas.grid()

    return canvas_frame, graph


def sprint_3_others(frame, sender):
    """
    creates the frame and widgets for all the sprint 3 gui parts except for the graph
    :param frame: the master frame
    :param sender: the mqtt client used by the buttons to send commands
    :return:
    """
    others_frame = ttk.Frame(frame)
    button = ttk.Button(others_frame, text='Sprint 3', width=100)
    button['command'] = lambda: sender.send_message('m3_sprint_3', [])
    button.grid(sticky='EWNS')

    return others_frame

# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------


main()
