#!/usr/bin/python  


#Code for turning off a 5V relay on GPIO 18 on and off three times,
#with a two second interval.
#The pin has to alternate between OUT and IN states instead of HIGH and LOW.
#Otherwise the relay will not turn off.
#OUT = active, IN = deactive

import RPi.GPIO as GPIO  
import time  
  
GPIO.setmode(GPIO.BCM)

for x in range(0,3):
	GPIO.setup(18, GPIO.OUT)
	time.sleep(2)
	GPIO.setup(18, GPIO.IN)
	time.sleep(2)

GPIO.cleanup()
