#!/usr/bin/python

#Tank movement script version 1.1
#By Matias Raisanen
#Works with PS3 controller.
#Left analog stick to move left track, right analog for right.


from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import sys
import time
import Robot
import PS3Controller


PS3Cont = PS3Controller.PS3Controller(
	controllerCallBack = None,
	joystickNo = 0,
	deadzone = 0.05,
	#deadzone = 0.14,	#Deadzone of 0.14 eliminates the accidental tiny nudges on the controller
	scale = 1,
	invertYAxis = True)	#Y-axis must be inverted in order for the thumbsticks to work intuitively (forward=positive, back=negative)

LEFT_TRIM = 0
RIGHT_TRIM = 0

speed = 255 	#This determines the speed multiplier of the DC motors. Use values 0-255
robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

#Next we define the controls:
#If the value of the thumbstick is zero or greater, move forward
#ElseIf the value is negative, move backward.
#int() converts the value into a non-decimal number to be used by the motor to determine speed


#Left Stick
def LeftThumbYCallBack(value):
	if (value) >= 0:
		robot.LT_forward(int(value*(1)*speed))
		#print "Left track forward: ", int(value*(1)*100),"%"	#Uncomment this line to see visual feedback
	elif (value) < 0:
		robot.LT_backward(int(value*(-1)*speed))
		#print "Left track backward: ", int(value*(-1)*100),"%"	#Uncomment this line to see visual feedback

PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.LTHUMBY,
        LeftThumbYCallBack)

#Right Stick
def RightThumbYCallBack(value):
        if (value) >= 0:
                robot.RT_forward(int(value*(1)*speed))
                #print "Right track forward: ", int(value*(1)*100),"%"   #Uncomment this line to see visual feedback
        elif (value) < 0:
                robot.RT_backward(int(value*(-1)*speed))
                #print "Right track backward: ", int(value*(-1)*100),"%" #Uncomment this line to see visual feedback

PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.RTHUMBY,
        RightThumbYCallBack)

#DPAD controls for camera
def DpadUpCallBack(value):
        if (value) > 0:
            print "Camera up"	#Uncomment this line to see visual feedback
        elif (value) == 0:
            print "Camera up STOP"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.DPADUP,
        DpadUpCallBack
        )

def DpadDownCallBack(value):
        if (value) > 0:
            print "Camera down"	#Uncomment this line to see visual feedback
        elif (value) == 0:
            print "Camera down STOP"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.DPADDOWN,
        DpadDownCallBack
        )

def DpadLeftCallBack(value):
        if (value) > 0:
            print "Camera left"	#Uncomment this line to see visual feedback
        elif (value) == 0:
            print "Camera left STOP"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.DPADLEFT,
        DpadLeftCallBack
        )

def DpadRightCallBack(value):
        if (value) > 0:
            print "Camera right"	#Uncomment this line to see visual feedback
        elif (value) == 0:
            print "Camera right STOP"	#Uncomment this line to see visual feedback

PS3Cont.setupControlCallback(
        PS3Cont.PS3Controls.DPADRIGHT,
        DpadRightCallBack
        )

#Press TRIANGLE to move forward at full speed (255)
def YButtonCallBack(value):
	if (value) > 0:
		robot.forward(255)
		print "FULL STEAM AHEAD!"	#Uncomment this line to see visual feedback
	PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.Y,
	YButtonCallBack)

#Press CIRCLE to stop motors
def StopButtonCallBack(value):
	if (value) > 0:
		robot.stop()
		print "Stop"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.SPHERE,
	StopButtonCallBack)

#Press CROSS
def CrossButtonCallBack(value):
	if (value) == 1:
		print "CROSS button pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.CROSS,
	CrossButtonCallBack)

#Press SQUARE
def SquareButtonCallBack(value):
	if (value) == 1:
		print "SQUARE button pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.SQUARE,
	SquareButtonCallBack)

#Press TRIANGLE
def TriangleButtonCallBack(value):
	if (value) == 1:
		print "TRIANGLE button pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.TRIANGLE,
	TriangleButtonCallBack)

#Press L1
def L1ButtonCallBack(value):
	if (value) == 1:
		print "L1 pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.L1,
	L1ButtonCallBack)

#Press R1
def R1ButtonCallBack(value):
	if (value) == 1:
		print "R1 button pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.R1,
	R1ButtonCallBack)
'''
#Press START
def StartButtonCallBack(value):
	if (value) == 1:
		print "Start pressed"	#Uncomment this line to see visual feedback
PS3Cont.setupControlCallback(
	PS3Cont.PS3Controls.START,
	StartButtonCallBack)
'''

#Next part runs the actual program:

try:
    #start the controller
	PS3Cont.start()
	#Cool visuals :-)
	print '\033[92m' + " "						#Green color
	print "*****************TANK CONTROL V 1.2*PS3***************"
	print "* Use analog sticks for left and right track control *"
	print "* Press CIRCLE to stop the tank                      *"
	print "* Press TRIANGLE to go full steam ahead              *"
	print "* CTRL + C to quit                                   *"
	print "******************************************************"
	print '\033[0m' + " "						#Default color
	print "Ready for input!"

	while True:
		time.sleep(1)

	#Ctrl C
except KeyboardInterrupt:
	print '\033[91m' + "\nEXIT via CTRL + C" + '\033[0m'	#Print in RED, then return to Defaults

	#error
except:
	print "Unexpected error:", sys.exc_info()[0]
	raise

finally:
	#stop the controller
	PS3Cont.stop()

#Sources:
#http://www.stuffaboutcode.com/2014/10/raspberry-pi-xbox-360-controller-python.html
#https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview
