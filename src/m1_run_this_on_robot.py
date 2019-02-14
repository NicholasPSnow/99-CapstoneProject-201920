"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Nicholas Snow.
  Winter term, 2018-2019.
"""
import rosebot as bot
import mqtt_remote_method_calls as com
import time
import m1_personal_delegate


def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    robot = bot.RoseBot()
    delegate=m1_personal_delegate.ROBOT_DelegateThatReceives(robot)
    mqtt_reciever=com.MqttClient(delegate)
    mqtt_reciever.connect_to_pc()
    while True:
        time.sleep(0.01)
        if delegate.is_Quit()==1:
            print("Quit Sucessful")
            break;
        if delegate.is_Exit()==1:
            print("Exit Sucessful")
            break;
    print("Program Has Ended")
# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()