import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)

p = GPIO.PWM(12,50)
p.start(6.5)

t = GPIO.PWM(16,50)
t.start(4)

sleeptime = 0.2

pcycle = 4
ppercent = 0
tcycle = 4
tpercent = 0

try:
	for i in range(11):
		print("Angle: %s%%" % (tpercent))
		print("DutyCycle: %s" % (tcycle))
		print("")
		t.ChangeDutyCycle(tcycle)
		tcycle += .5
		tpercent += 10
		time.sleep(sleeptime)
	t.ChangeDutyCycle(4)
	time.sleep(1)

	for i in range(11):
		print("Angle: %s%%" % (ppercent))
		print("DutyCycle: %s" % (pcycle))
		print("")
		p.ChangeDutyCycle(pcycle)
		pcycle += .5
		ppercent += 10
		time.sleep(sleeptime)
	p.ChangeDutyCycle(6.5)
	time.sleep(0.5)

except KeyboardInterrupt:
	p.stop()
	t.stop()
	GPIO.cleanup()

finally:
	p.stop()
	t.stop()
	GPIO.cleanup()
	quit()

