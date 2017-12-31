#!/usr/bin/python

#Tank movement script version 1.1
#By Matias Raisanen
#Works with Xbox controller.
#Left analog stick to move left track, right analog for right.

#Before running this script, you should type  "sudo xboxdrv --silent --detach-kernel-driver &" into console

from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import sys
import time
import Robot
import XboxController

xboxCont = XboxController.XboxController(
	controllerCallBack = None,
	joystickNo = 0,
	deadzone = 0.14,	#Deadzone of 0.14 eliminates the accidental tiny nudges on the controller
	scale = 1,
	invertYAxis = True)	#Y-axis must be inverted in order for the thumbsticks to work intuitively (forward=positive, back=negative)

LEFT_TRIM = 0
RIGHT_TRIM = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)

#Next we define the controls:
#If the value of the thumbstick is zero or greater, move forward
#ElseIf the value is negative, move backward.
#int() converts the value into a non-decimal number to be used by the motor to determine speed


#Left Stick
def LeftThumbYCallBack(value):
	if (value) >= 0:
		robot.LT_forward(int(value*(1)*200))  #200 determines the speed of the motor (0-255)
		#print "Left track forward: ", int(value*(1)*100),"%"	#Uncomment this line to see visual feedback
	elif (value) < 0:
		robot.LT_backward(int(value*(-1)*200))
		#print "Left track backward: ", int(value*(-1)*100),"%"	#Uncomment this line to see visual feedback

xboxCont.setupControlCallback(
        xboxCont.XboxControls.LTHUMBY,
        LeftThumbYCallBack)

#Right Stick
def RightThumbYCallBack(value):
        if (value) >= 0:
                robot.RT_forward(int(value*(1)*200))
                #print "Right track forward: ", int(value*(1)*100),"%"	#Uncomment this line to see visual feedback
        elif (value) < 0:
                robot.RT_backward(int(value*(-1)*200))
                #print "Right track backward: ", int(value*(-1)*100),"%"	#Uncomment this line to see visual feedback

xboxCont.setupControlCallback(
        xboxCont.XboxControls.RTHUMBY,
        RightThumbYCallBack)

#Use Dpad to turn (the camera)
#Camera movement not yet implemented
def DpadCallBack(value):
	x = 100

	if (value) == (-1, 0):		#Dpad left
		print "Pan left"
		robot.RT_forward(x)
		robot.LT_backward(x)
		print ""
	elif (value) == (1, 0):		#Dpad right
		print "Pan right"
		robot.LT_forward(x)
		robot.RT_backward(x)
		print ""
	elif (value) == (0, 1):		#Dpad up
		print "Camera up!"
		print ""
	elif (value) == (0, -1):
		print "Camera down!"	#Dpad down
		print ""
	elif (value) == (1, 1):		#Dpad up right
		print "Camera up!"
		print "Pan right!"
		robot.LT_forward(x)
		robot.RT_backward(x)
		print ""
	elif (value) == (1, -1):	#Dpad down right
		print "Camera down!"
		print "Pan right!"
		robot.LT_forward(x)
		robot.RT_backward(x)
		print ""
	elif (value) == (-1, 1):	#Dpad up left
		print "Camera up!"
		print "Pan left!"
		robot.RT_forward(x)
		robot.LT_backward(x)
		print ""
	elif (value) == (-1, -1):	#Dpad down left
		print "Camera down!"
		print "Pan left!"
		robot.RT_forward(x)
		robot.LT_backward(x)
		print ""

	elif (value) == (0, 0):
			robot.stop()

xboxCont.setupControlCallback(
        xboxCont.XboxControls.DPAD,
        DpadCallBack)	

#Press Y to move forward at full speed (255)
def YButtonCallBack(value):
	if (value) > 0:
		robot.forward(255)
		#print "FULL STEAM AHEAD!"	#Uncomment this line to see visual feedback
	xboxCont.setupControlCallback(
	xboxCont.XboxControls.Y,
	YButtonCallBack)

#Press B to stop motors
def StopButtonCallBack(value):
	if (value) > 0:
		robot.stop()
		#print "Stop"	#Uncomment this line to see visual feedback
xboxCont.setupControlCallback(
	xboxCont.XboxControls.B,
	StopButtonCallBack)

#Press Select to stop motors
def BackButtonCallBack(value):
        if (value) > 0:
                robot.stop()
                #print "Stop"	#Uncomment this line to see visual feedback

xboxCont.setupControlCallback(
	xboxCont.XboxControls.BACK,
	BackButtonCallBack)


#Next part runs the actual program:

try:
    #start the controller
	xboxCont.start()
	#Cool visuals :-)
	print '\033[92m' + " "						#Green color
	print "*****************TANK CONTROL V 1.1*******************"
	print "* Use analog sticks for left and right track control *"
	print "* Press B to stop the tank                           *"
	print "* Press Y to go full steam ahead                     *"
	print "* CTRL + C to quit                                   *"
	print "******************************************************"
	print '\033[0m' + " "						#Default color
	print "Xbox controller detected, ready for input!"

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
	xboxCont.stop()

#Sources:
#http://www.stuffaboutcode.com/2014/10/raspberry-pi-xbox-360-controller-python.html
#https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/overview
