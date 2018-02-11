import RPi.GPIO as GPIO
import time
from Adafruit_PWM_Servo_Driver import PWM
import Robot
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Sonar based on: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

'''
Bot functions as follows:
Execute a distance scan every 50ms.
If distance to object is greater than 20cm, drive forward.
If distance is less than 20cm, stop and execute a sweeping scan in 180 degree arc, starting from right
to left. Start scanning for a direction, where distance to object is greater than 25.
If found, turn the bot. If not found, turn around fully.
'''

TRIG = 18 
ECHO = 16

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

pwm = PWM(0x40)
panCenter = 365 #Pan servo, center position
tiltCenter = 420
panMAX = 610  #Leftmost position
panMIN = 150  #Rightmost position


pwm.setPWMFreq(60)
pwm.setPWM(3, 0, 470) #Start tilt servo at a slight downward angle.
pwm.setPWM(2, 0, panCenter)  #Start pan servo at center

robot = Robot.Robot(left_trim=0, right_trim=0)

def laserOn():
	GPIO.setup(7, GPIO.OUT)

def laserOff():
	GPIO.setup(7, GPIO.IN)


def measureDist():
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
	  pulse_start = time.time()

	while GPIO.input(ECHO)==1:
	  pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)

	return distance

def sonarSweep():
	'''Make a 180 degree sweep, and measure distance at every 45 degrees'''
	sonarAngle = 150						#Start on the right, or 0 degrees
	pwm.setPWM(2, 0, sonarAngle)
	time.sleep(.2)
	laserOn()
	distance = measureDist()				#Measure distance to object
	#print "First measure: ", distance
	time.sleep(.2)

	#Next we want to find out a direction to turn to
	if distance < 25:						#If object is closer than 25cm, turn the sonar
		sonarAngle = 110					#Change angle value to 110. Servo angle values are not directly proportional to their values in degrees, hence the manual change here.
		while distance < 25:				
			#print "Too close: ", distance
			sonarAngle = sonarAngle + 125	#Increment the angle by 125, through 150, 235, 365, 485 and 610

			if sonarAngle > 610:			#If we exceed maximum angle of 610, turn the whole robot on the spot
				#print("No room! Turn around")
				pwm.setPWM(2, 0, panCenter)	
				break

			pwm.setPWM(2, 0, sonarAngle)	#Turn the sonar to the new angle
			#print "Let's try a new angle:", sonarAngle
			time.sleep(.2)
			distance = measureDist()		#Scan for objects
			#print "New measure: ", distance
			time.sleep(.1)
	pwm.setPWM(2, 0, panCenter)
	time.sleep(.5)
	
	#Next we start turning into the direction, until we have at least 30cm room.
	
	if sonarAngle < 360:	#Turn right
		distance = measureDist()
		time.sleep(.2)
		while distance < 30:
			robot.RT_backward(150)
			robot.LT_forward(150)
			distance = measureDist()
			time.sleep(.5)
		laserOff()
		robot.stop()
		return "dist below 30"

	elif sonarAngle > 360:	#Turn left
		distance = measureDist()
		time.sleep(.2)
		while distance < 30:
			robot.RT_forward(150)
			robot.LT_backward(150)
			distance = measureDist()
			time.sleep(.5)
		laserOff()
		robot.stop()
		return "dist above 30"
	else:
		laserOff()
		return "Something Went Wrong"

def sonarSweep2():
	'''Measure distance at 45 and 135 degrees, compare them, and turn in the direction of the greater value'''

	sonarAngle = 235						#Measure on the right, at 45 degrees
	pwm.setPWM(2, 0, sonarAngle)
	time.sleep(.2)
	laserOn()
	distanceRight = measureDist()
	#print "Distance on right: ", distanceRight
	time.sleep(.2)

	sonarAngle = 485						#Measure on the left at 135 degrees
	pwm.setPWM(2, 0, sonarAngle)
	time.sleep(.2)
	distanceLeft = measureDist()
	#print "Distance on left: ", distanceLeft
	time.sleep(.2)

	sonarAngle = panCenter					#Return the sonar to center
	pwm.setPWM(2, 0, sonarAngle)
	time.sleep(.2)

	#Next we want to find out a direction to turn to
	if distanceRight > distanceLeft:	#Compare values, and choose the direction of turn
		distance = measureDist()
		time.sleep(.2)
		while distance < 30:	#Turn right until clearance is at least 30cm.
			robot.RT_backward(150)
			robot.LT_forward(150)
			distance = measureDist()
			time.sleep(.5)
		laserOff()
		robot.stop()
		return "Right turn complete"

	else:						#Turn left until clearance of at least 30cm.
		distance = measureDist()
		time.sleep(.2)
		while distance < 30:
			robot.RT_forward(150)
			robot.LT_backward(150)
			distance = measureDist()
			time.sleep(.5)
		laserOff()
		robot.stop()
		return "Left turn complete"


def moveBot():

	running = True
	botSpeed = 200

	
	while running:
		distance = measureDist()
		if distance > 20:
			#print "Forward. Distance: ", distance
			robot.RT_forward(botSpeed)
			robot.LT_forward(botSpeed)
		else:
			#print "Stop. Distance: ", distance
			robot.stop()
			result = sonarSweep2()
			#print result
		time.sleep(.5)
	
	print("Stop")
	robot.stop()
	
def main():
	moveBot()
	GPIO.cleanup()
	
if __name__ == "__main__":
	main()