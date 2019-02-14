"""
  Capstone Project.  Code to run on the EV3 robot (NOT on a laptop).
  This code is the delegate for handling messages from the shared GUI.

  Author:  Your professors (for the framework)
    and Nicholas Snow, Katana Colledge, and Zach Kelly.
  Winter term, 2018-2019.
"""

import rosebot as bot
import mqtt_remote_method_calls as com
import time
import math
import m3_run_this_on_robot as m3


class DelegateThatReceives(object):

    def __init__(self, robot):
        self.robot = bot.RoseBot()
        self.Quit=0
        self.Exit=0

    def is_Quit(self):
        if self.Quit==1:
            self.stop()
            self.down()
        return self.Quit

    def is_Exit(self):
        if self.Quit == 1:
            self.stop()
            self.down()
        return self.Exit

    ##DRIVE SYSTEM
    #Handle Quit and Exit
    def command(self,argument):
        print("Command Recieved: ",argument)
        if argument == "quit":
            print("Quit")
            self.Quit = 1

        if argument == 'exit':
            print("Exit")
            self.Exit = 1

    def stop(self):
        print("Command Recieved: Stop")
        self.robot.drive_system.stop()


    #Handle Forward and Backward and Left and Right
    def movement(self, left_speed, right_speed):
        print("Command Recieved: Movement",left_speed,right_speed)
        self.robot.drive_system.go(int(left_speed), int(right_speed))

    ##ARM SYSTEM
    def up(self):
        print("Command Recieved: Up")
        self.robot.arm_and_claw.raise_arm()

    def down(self):
        print("Command Recieved: Down")
        self.robot.arm_and_claw.lower_arm()

    def move_to_pos(self,position):
        print("Command Recieved: Move to Position",position)
        integerposition= int(position)
        if integerposition <=10:
            integerposition = 10
        self.robot.arm_and_claw.move_arm_to_position(integerposition)

    def calibrate(self):
        print("Command Recieved: Calibrate Arm")
        self.robot.arm_and_claw.calibrate_arm()


    # IR Sensor

    def ir_forward(self, inches, speed):
        print("Command Received: Go forward until distance is less than")
        self.robot.drive_system.go_forward_until_distance_is_less_than(inches, speed)

    def ir_backward(self, inches, speed):
        print("Command Received: Go backward until distance is greater than")
        self.robot.drive_system.go_backward_until_distance_is_greater_than(inches, speed)

    def ir_within_dist(self, inches, speed):
        print("Command Received: Go until distance is within")
        self.robot.drive_system.go_until_distance_is_within(inches, speed)

    ##Sprint 1 SYSTEM

    def Forward_Time(self,speed,time):
        print("Command Recieved: Forward_Time")
        self.robot.drive_system.go_straight_for_seconds(int(time),int(speed))
    def Forward_Time_Inches(self,speed,inches):
        print("Command Recieved: Forward_Time_Inches")
        self.robot.drive_system.go_straight_for_inches_using_time(int(inches),int(speed))
    def Forward_Inches(self,speed,inches):
        print("Command Recieved: Forward_Inches")
        self.robot.drive_system.go_straight_for_inches_using_encoder(int(inches),int(speed))

    def beep_button(self,numberofbeeps):
        print("Command Recieved: Beep")
        for k in range(int(numberofbeeps)):
            self.robot.sound_system.beeper.beep()
    def tone_button(self,duration,frequency):
        print("Command Recieved: Tone")
        self.robot.sound_system.tone_maker.play_tone(frequency,duration)

    def speak_button(self,text):
        print("Command Recieved: Speak")
        self.robot.sound_system.speech_maker.speak(text)

## Katana'S GUI Handler

    def obtain_with_sensor_button(self, speed_str, rate_of_increase_str, initial_frequency_str):

        print("Command Recieved: obtain_with_sensor")

        increase_frequency = int(rate_of_increase_str)
        speed = int(speed_str)
        duration = 5
        frequency = int(initial_frequency_str)

        print("Retrieving Object")
        #self.robot.arm_and_claw.calibrate_arm()
        self.robot.sound_system.tone_maker.play_tone(frequency,duration)
        self.robot.drive_system.go(speed,speed)
        inches = 5
        while True:
            distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
            counter_agree=0
            counter_disagree = 0
            #frequency = frequency + increase_frequency
            #self.robot.sound_system.tone_maker.play_tone(frequency, duration)
            while distance < inches:
                distance = self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches()
                print(counter_disagree,counter_agree)
                if distance > inches:
                    counter_disagree = counter_disagree+1
                else:
                    counter_agree = counter_agree+1
                if counter_agree >= 3:
                    break
                if counter_disagree >= 3:
                    break
            if counter_agree >= 3:
                break
        self.robot.drive_system.stop()
        #self.robot.arm_and_claw.raise_arm()
        print("Obtained Object")
        #victory = [100,200,300,400,300,400]
        #self.robot.sound_system.tone_maker.play_tone_sequence(victory)


    def obtain_with_camera_button(self,wheel_speed_str,spin_speed_str,spin_direction,rate_of_increase_str, initial_frequency_str):

        print("Command Recieved: Camera obtain")

        self.robot.arm_and_claw.lower_arm()
        wheel_speed = int(wheel_speed_str)
        spin_speed = int(spin_speed_str)
        direction = str(spin_direction)
        increase_frequency = int(rate_of_increase_str)
        inital_frequency = int(initial_frequency_str)

        if direction == 'Clockwise':
            self.robot.drive_system.spin_clockwise_until_sees_object(spin_speed,20)
            self.obtain_with_sensor_button(wheel_speed,increase_frequency,inital_frequency)
        elif direction == 'Counter Clockwise':
            self.robot.drive_system.spin_counterclockwise_until_sees_object(spin_speed,20)
            self.obtain_with_sensor_button(wheel_speed,increase_frequency,inital_frequency)
        else:
            print('Incorrect direction value. Please input "Clockwise" or "Counter Clockwise"')
            pass



    ## NICK'S GUI HANDLER

    def m1proximity_button(self,rate_of_beeps, initial_beeps):
        print("Command Recieved: Proximity")
        self.robot.arm_and_claw.lower_arm()
        int_initial_beeps=int(initial_beeps)
        int_rate_of_beeps=int(rate_of_beeps)

        self.robot.drive_system.go(75, 75)
        print("Searching")
        while self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches() >= 4:
            print("Delay is: ",(int(initial_beeps)/(int(rate_of_beeps)*self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())))
            time.sleep((int(initial_beeps)/(int(rate_of_beeps)*self.robot.sensor_system.ir_proximity_sensor.get_distance_in_inches())))
            self.robot.sound_system.beeper.beep()
        print("Object Found")
        self.robot.arm_and_claw.raise_arm()
        self.robot.drive_system.stop()

    def m1camera_button(self,speed,direction,rate_of_beeps, initial_beeps):
        print("Command Recieved: Camera")

        if direction=="Clockwise":
            self.robot.drive_system.spin_clockwise_until_sees_object(speed, 20)

        if direction=="Counter-Clockwise":
            self.robot.drive_system.spin_counterclockwise_until_sees_object(speed, 20)

        self.proximity_button(rate_of_beeps,initial_beeps)

    def m1line_button(self,starting_side):
        print("Command Recieved: Line")
        original = self.robot.sensor_system.color_sensor.get_reflected_light_intensity()

        while self.Exit == 0  and self.Quit == 0:
            current = self.robot.sensor_system.color_sensor.get_reflected_light_intensity()

            if starting_side=='Right':
                if original <=current+2 and original >=current-2:
                    self.robot.drive_system.go(50,50)
                else:
                    self.robot.drive_system.go(-50,50)

            if starting_side=='Left':
                if original <=current+2 and original >=current-2:
                    self.robot.drive_system.go(50,50)
                else:
                    self.robot.drive_system.go(50,-50)



## COlOR GUI HANDLER
    def intensity_less_button(self,speed, intensity):
        print("Command Recieved: Intensity Less Than")
        self.robot.drive_system.go_straight_until_intensity_is_less_than(int(intensity),int(speed))
    def intensity_greater_button(self,speed, intensity):
        print("Command Recieved: Intensity Greater Than")
        self.robot.drive_system.go_straight_until_intensity_is_greater_than(int(intensity),int(speed))
    def until_color_button(self,speed, color):
        print("Command Recieved: Until Color", color, self.robot.sensor_system.color_sensor.get_color_number_from_color_name(color))
        self.robot.drive_system.go_straight_until_color_is(self.robot.sensor_system.color_sensor.get_color_number_from_color_name(color), int(speed))
    def until_not_color_button(self, speed, color):
        print("Command Recieved: Until Not Color", color, self.robot.sensor_system.color_sensor.get_color_number_from_color_name(color))
        self.robot.drive_system.go_straight_until_color_is_not(self.robot.sensor_system.color_sensor.get_color_number_from_color_name(color),int(speed))

## Proximity GUI HANDLER
    def distance_greater_button(self,speed, inches):
        print("Command Recieved: Until Distance Greater")
        self.robot.drive_system.go_backward_until_distance_is_greater_than(int(inches),int(speed))

    def distance_less_button(self,speed, inches):
        print("Command Recieved: Until Distance Less")
        self.robot.drive_system.go_forward_until_distance_is_less_than(int(inches),int(speed))

    def until_distance_button(self,speed, inches, delta):
        print("Command Recieved: Until Within Delta")
        self.robot.drive_system.go_until_distance_is_within(int(delta),int(inches),int(speed))


##CAMERA GUI HANDLER

    def camera_counter_clockwise_button(self,speed, area):
        print("Command Recieved: Camera Search CCW")
        self.robot.drive_system.spin_counterclockwise_until_sees_object(int(speed),int(area))
    def camera_clockwise_button(self,speed, area):
        print("Command Recieved: Camera Search CW")
        self.robot.drive_system.spin_clockwise_until_sees_object(int(speed),int(area))

    # -------------------------------------------------------------------------
    # Zach's Sprint 2 Handlers
    # -------------------------------------------------------------------------

    def m3_feature_9(self, init_rate, acceleration):
        print("Command Received: M3 Feature 9")
        m3.feature_9(self.robot, init_rate, acceleration)

    def m3_feature_10(self, speed, direction):
        print("Command Received: M3 Feature 10")
        m3.feature_10(self.robot, speed, direction)
