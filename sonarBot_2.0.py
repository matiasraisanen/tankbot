import RPi.GPIO as GPIO
import time
from Adafruit_PWM_Servo_Driver import PWM
import Robot
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Sonar based on: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

'''
Bot functions as follows:
Measure distance.
If distance to object is greater than 20cm, drive forward.
Execute a new scan every 10ms.
If distance is less than 20cm, stop and execute a sweeping scan in 180 degree arc, from right
to left. Start scanning for a direction, where distance to object is greater than 25.
If found, turn the bot. If not found, turn around fully.
'''

TRIG = 18 
ECHO = 16

print "Sonar sweep 1.0"
print "***\n"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)

pwm = PWM(0x40)
panCenter = 365 #Pan servo, center position
panMAX = 610  #Leftmost position
panMIN = 150  #Rightmost position


pwm.setPWMFreq(60)
pwm.setPWM(3, 0, 420) #Start servos centered
pwm.setPWM(2, 0, panCenter)  #Start pan servo at center

robot = Robot.Robot(left_trim=0, right_trim=0)

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
	distance = measureDist()				#Measure distance to object
	print "First measure: ", distance
	time.sleep(.2)

	if distance < 25:						#If object is closer than 25cm, turn the sonar
		sonarAngle = 110					#Change angle value to 110. Servo angle values are not directly proportional to their values in degrees, hence the manual change here.
		while distance < 25:				
			print "Too close: ", distance
			sonarAngle = sonarAngle + 125	#Increment the angle by 125, through 150, 235, 365, 485 and 610

			if sonarAngle > 610:			#If we exceed maximum angle of 610, turn the whole robot on the spot
				print("No room! Turn around")
				pwm.setPWM(2, 0, panCenter)	
				return "FullTurn"

			pwm.setPWM(2, 0, sonarAngle)	#Turn the sonar to the new angle
			print "Let's try a new angle:", sonarAngle
			time.sleep(.2)
			distance = measureDist()		#Scan for objects
			print "New measure: ", distance
			time.sleep(.1)
	else:
		pass
	pwm.setPWM(2, 0, panCenter)
	
	if sonarAngle == 150:
		return "HardRight"
	elif sonarAngle == 235:
		return "Right"
	elif sonarAngle == 360:
		return "Straight"
	elif sonarAngle == 485:
		return "Left"
	elif sonarAngle == 610:
		return "HardLeft"
	else:
		return "Something Went Wrong"

def moveBot():
	shortTime = 1
	longTime = 2
	fullTurn = 3
	running = True
	botSpeed = 75


	while running:
		distance = measureDist()
		if distance > 20:
			print "Forward. Distance: ", distance
			robot.RT_forward(botSpeed)
			robot.LT_forward(botSpeed)
		else:
			print "Stop. Distance: ", distance
			robot.stop()
			result = sonarSweep()
			print "sonarSweep suoritettu: ", result, "\n"

			if result == "HardRight":
				robot.RT_backward(botSpeed)
				robot.LT_forward(botSpeed)
				time.sleep(longTime)
			if result == "Right":
				robot.RT_backward(botSpeed)
				robot.LT_forward(botSpeed)
				time.sleep(shortTime)
			if result == "HardLeft":
				robot.RT_forward(botSpeed)
				robot.LT_backward(botSpeed)
				time.sleep(longTime)
			if result == "Left":
				robot.RT_forward(botSpeed)
				robot.LT_backward(botSpeed)
				time.sleep(shortTime)
			if result == "FullTurn":
				robot.RT_backward(botSpeed)
				robot.LT_forward(botSpeed)
				time.sleep(fullTurn)				



		time.sleep(.5)

	print("Stop")
	robot.stop()

moveBot()
GPIO.cleanup()
robot.stop()