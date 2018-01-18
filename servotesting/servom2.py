import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

#p = GPIO.PWM(12,50)
#p.start(7.5)

t = GPIO.PWM(16,50)
t.start(8)

try:
	while True:
		#p.ChangeDutyCycle(6.5)
		t.ChangeDutyCycle(8)
		#time.sleep(1)
		#p.ChangeDutyCycle(11.5)
		#t.ChangeDutyCycle(11.5)
		#time.sleep(1)
		#p.ChangeDutyCycle(2.5)
		#t.ChangeDutyCycle(4)
		#time.sleep(1)

except KeyboardInterrupt:
#	p.stop()
	t.stop()
	GPIO.cleanup()