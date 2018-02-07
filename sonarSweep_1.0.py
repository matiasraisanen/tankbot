import RPi.GPIO as GPIO
import time
from Adafruit_PWM_Servo_Driver import PWM
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#Sonar based on: https://www.modmypi.com/blog/hc-sr04-ultrasonic-range-sensor-on-the-raspberry-pi

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
	startTime = time.time()
	panServo = 145
	turnPerTick = 5 #Turning speed
	turnCounter = -1
	pwm.setPWM(2, 0, panMIN)
	time.sleep(.5)
	while panServo < panMAX:
		panServo += turnPerTick
		pwm.setPWM(2, 0, panServo)
		turnCounter += 1
		if (panServo == 150) or (panServo == 235) or (panServo == 365) or (panServo == 485) or (panServo == 610):
			print "ServoPos: ",panServo
			result = measureDist()
			print "Distance: ",result
			print ""
			#time.sleep(1)
		time.sleep(.01)

	print "Total turns: ",turnCounter
	endTime = time.time()
	runTime = endTime - startTime
	print "Runtime: ",runTime
	pwm.setPWM(2, 0, panCenter)

sonarSweep()

GPIO.cleanup()