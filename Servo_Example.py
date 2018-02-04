#!/usr/bin/python

from Adafruit_PWM_Servo_Driver import PWM
import time

# ===========================================================================
# Example Code
# ===========================================================================

# Initialise the PWM device using the default address
#pwm = PWM(0x40)
# Note if you'd like more debug output you can instead run:
pwm = PWM(0x40, debug=False)

tiltUp = 220  # Min pulse length out of 4096
tiltDown = 530  # Max pulse length out of 4096
tiltCenter = 420

panRight = 150
panCenter = 360
panLeft = 580

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 40                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)


#Servo no.3 is tilt
#Servo no.2 is pan

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
while (True):
  # Change speed of continuous servo on channel O
  
  print("servoRight")
  pwm.setPWM(2, 0, panRight)
  time.sleep(1)
  
  print("Center")
  pwm.setPWM(2, 0, panCenter)
  time.sleep(1)
  
  print("servoLeft")
  pwm.setPWM(2, 0, panLeft)
  time.sleep(1)
  
  '''
  print("servoUp")
  pwm.setPWM(3, 0, tiltUp)
  time.sleep(1)
  print("Center")
  pwm.setPWM(3, 0, tiltCenter)
  time.sleep(1)
  print("servoDown")
  pwm.setPWM(3, 0, tiltDown)
  time.sleep(1)
  '''

