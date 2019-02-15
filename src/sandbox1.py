"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  Author:  Your professors (for the framework)
    and Nicholas Snow.
  Winter term, 2018-2019.
"""
import rosebot as bot
import mqtt_remote_method_calls as com
import time
import math
def main():
    """
    This code, which must run on the EV3 ROBOT:
      1. Makes the EV3 robot to various things.
      2. Communicates via MQTT with the GUI code that runs on the LAPTOP.
    """

    robot = bot.RoseBot()
    path=[250,250,10,10,20,20]
    x=250
    y=250
    print("Run")

    for k in range(2, len(path)-1, 2):
        print(x,y, path[k], path[k + 1])
        #goto_point(x, y, path[k], path[k + 1])
        x = path[k]
        y = path[k + 1]
    print("Done")



def rotate_right(self,angle):
    self.left_motor.reset_position()
    self.go(100, 0)
    while True:
        degrees = self.left_motor.get_position()
        if abs(degrees) >= (2.5*360*(angle)/90):
            break
    self.stop()


def rotate_left(self,angle):
    self.right_motor.reset_position()
    self.go(0, 100)
    while True:
        degrees = self.right_motor.get_position()
        if abs(degrees) >= (2.5*360*(angle)/90):
            break
    self.stop()

def goto_point(currentx,currenty,newx,newy):
    currentintx=int(currentx)
    currentinty=int(currenty)
    newintx=int(newx)
    newinty=int(newy)
    distance = math.sqrt((abs(currentintx-newintx)) ** 2 + (abs(currentinty-newinty)) ** 2)/6
    angle = 45
    rotate_left(angle)
    bot.DriveSystem.go_straight_for_inches_using_encoder(distance,100)
    rotate_right(angle+90)




# -----------------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# -----------------------------------------------------------------------------
main()