#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor

import time
import atexit
import curses
import Robot

LEFT_TRIM = 0
RIGHT_TRIM = 0

robot = Robot.Robot(left_trim=LEFT_TRIM, right_trim=RIGHT_TRIM)


screen = curses.initscr()
curses.noecho()
curses.cbreak()
screen.keypad(True)

try:
        print "Robot control script v 1.0"
        print "Use arrow keys to move"
        print "Press SPACEBAR to stop moving"
        print "Exit by pressing ctrl + c"
	while True:
	 char = screen.getch()

	 if char == ord('q'):
		break
	 elif char == curses.KEY_UP:
		#print "up"
		robot.forward(200)
	 elif char == curses.KEY_DOWN:
		#print "down"
		robot.backward(200)
	 elif char == curses.KEY_RIGHT:
		#print "right"		#mirrored :-D
		robot.left(150)
	 elif char == curses.KEY_LEFT:
		#print "left"
		robot.right(150)	#mirrored :-D
	 elif char == 32:
		#print "stop"		#press SPACEBAR to stop moving
		robot.stop()
finally:
    #Close down curses properly, inc turn echo back on!
    curses.nocbreak(); screen.keypad(0); curses.echo()
    curses.endwin()
    print "Exiting..."

