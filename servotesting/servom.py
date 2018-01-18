import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)

frequencyHertz = 50
pwm = GPIO.PWM(12, frequencyHertz)

leftPosition = 0.75
rightPosition = 2.5
middlePosition = (rightPosition - leftPosition) / 2 + leftPosition

positionList = [leftPosition, middlePosition, rightPosition, middlePosition]

mspercycle = 1000 / frequencyHertz

# Iterate through the positions sequence 3 times.
for i in range(3):
	# This sequence contains positions from left to right
	# and then back again.  Move the motor to each position in order.
	for position in positionList:
		duty_cycle_percentage = position * 100 / mspercycle
		print("Position: " + str(position))
		print("Duty Cycle: " + str(duty_cycle_percentage))
		print("")
		pwm.start(duty_cycle_percentage)
		time.sleep(.5)
	

# Done.  Terminate all signals and relax the motor.
pwm.stop()

# We have shut all our stuff down but we should do a complete
# close on all GPIO stuff.  There's only one copy of real hardware.
# We need to be polite and put it back the way we found it.
GPIO.cleanup()