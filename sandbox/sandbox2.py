# Put whatever you want in this module and do whatever you want with it.
# It exists here as a place where you can "try out" things without harm.

def get_IR_frame(window, mqtt_sender):
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
    frame_label = ttk.Label(frame, text="Infrared System")
    distance_is_less_than_label = ttk.Label(frame, text="Move Towards an Object")
    distance_is_greater_than_label = ttk.Label(frame, text="Move Away from an Object")
    distance_is_within_label = ttk.Label(frame, text="Move Until Object is Within Distance")

    distance_less = ttk.Entry(frame, width=8)
    distance_less.insert(0, "10")
    distance_greater = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    distance_greater.insert(0, "10")
    distance_within = ttk.Entry(frame, width=8, justify=tkinter.RIGHT)
    distance_within.insert(0, "10")

    distance_less_button = ttk.Button(frame, text="Move Towards")
    distance_greater_button = ttk.Button(frame, text="Move Away")
    distance_within_button = ttk.Button(frame, text="Move Near")

    # Grid the widgets:
    frame_label.grid(row=0, column=1)
    distance_is_less_than_label.grid(row=1, column=0)
    distance_is_less_than_label.grid(row=1, column=1)
    distance_is_greater_than_label.grid(row=1, column=2)
    distance_is_within_label.grid(row=1, column=3)

    distance_less.grid(row=2, column=0)
    distance_greater.grid(row=2, column=1)
    distance_within.grid(row=2, column=2)

    distance_less_button.grid(row=3, column=0)
    distance_greater_button.grid(row=3, column=1)
    distance_within_button.grid(row=3, column=2)

    # Set the button callbacks:
    distance_less_button["command"] = lambda: handle_distance_less_button(distance_less.get(),wheel_speed_entry.get(), mqtt_sender)
    distance_greater_button["command"] = lambda: handle_distance_greater_button(distance_greater.get(),wheel_speed_entry.get(), mqtt_sender)
    distance_within_button["command"] = lambda: handle_distance_within_button(distance_within.get(),wheel_speed_entry.get(), mqtt_sender)
    return

##############################################################
def handle_distance_less_button(inches,speed,mqtt_sender):
    mqtt_sender.send_message('distance_less', [str(inches), str(speed)])
    print('distance_less', inches, speed)

def handle_distance_greater_button(inches,speed,mqtt_sender):
    mqtt_sender.send_message('distance_greater', [str(inches), str(speed)])
    print('distance_greater', inches, speed)

def handle_distance_within_button(inches,speed,mqtt_sender):
    mqtt_sender.send_message('distance_within', [str(inches), str(speed)])
    print('distance_within', inches, speed)

##################################################################
def distance_less(self,inches,speed):
    print("Command Recieved: distance_less")
    self.robot.drive_system.go_forward_until_distance_is_less_than(int(inches),int(speed))

def distance_greater(self,inches,speed):
    print("Command Recieved: distance_greater")
    self.robot.drive_system.go_backward_until_distance_is_greater_than(int(inches),int(speed))

def distance_greater(self, inches, speed):
    print("Command Recieved: distance_greater")
    self.robot.drive_system.go_backward_until_distance_is_greater_than(int(inches), int(speed))
go_until_distance_is_within