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
    tone_frequency_label.grid(row=1, column=2)
    speak_text_label.grid(row=1, column=3)

    distance_less.grid(row=2, column=0)
    tone_duration.grid(row=2, column=1)
    tone_frequency.grid(row=2, column=2)
    speak_text.grid(row=2, column=3)

    distance_less_button.grid(row=3, column=0)
    tone_button.grid(row=3, column=1)
    speak_button.grid(row=3, column=3)

    # Set the button callbacks:
    distance_less_button["command"] = lambda: handle_beep_button(number_of_beeps.get(), mqtt_sender)
    tone_button["command"] = lambda: handle_tone_button(tone_duration.get(), tone_frequency.get(), mqtt_sender)
    speak_button["command"] = lambda: handle_speak_button(speak_text.get(), mqtt_sender)
    return frame