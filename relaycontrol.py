#!/usr/bin/python  
import RPi.GPIO as GPIO  
import time  
  
GPIO.setmode(GPIO.BCM)

for x in range(0,3):
	GPIO.setup(18, GPIO.OUT)
	time.sleep(2)
	GPIO.setup(18, GPIO.IN)
	time.sleep(2)

GPIO.cleanup()