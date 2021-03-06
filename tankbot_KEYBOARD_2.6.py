#Improved KEYBOARD control with WASD.
#FORWARD plus TURN results in a slow turn.
#TURN results in faster turn.
#2.0	Keys can be held down
#2.5	Start implementing camera commands. Camera servos connected to GPIO pins
#2.6  Servo control moved over to Servo Controller board. Added laser to SPACEBAR and GPIO 7

from Adafruit_PWM_Servo_Driver import PWM
import pygame
import os, sys
import Robot
import threading
import RPi.GPIO as GPIO
import time
import sonarBot

GPIO.setmode(GPIO.BOARD)

#Servo setup:
#Connect PAN servo to slot 2 and TILT servo to slot 3

pwm = PWM(0x40)
panServo = 365  #Pan servo, center position
tiltServo = 420 #Tilt servo, center position

panMAX = 610  #Leftmost position
panMIN = 150  #Rightmost position

tiltMAX = 530 #Downmost position
tiltMIN = 220 #Upmost position

servoSpeed = 5 #Turning speed

pwm.setPWMFreq(60)
pwm.setPWM(3, 0, tiltServo) #Start servos centered
pwm.setPWM(2, 0, panServo)  #Start servos centered

#END servo setup


speed = 255	#Speed multiplier, values 0-255
reducedSpeed = int(speed*0.50)  #Alternate track speed for turning. The lower the percentage, the lower the turning radius and forward momentum.
robot = Robot.Robot(left_trim=0, right_trim=0)
sonarBot = sonarBot

#os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
myfont = pygame.font.SysFont("monospace", 24)
screen = pygame.display.set_mode((200, 200))

running = True

#Dictionary for command values.
#The use of a dictionary helps us to read multiple values at the same time,
#and to specify an action related to their value.

moveCommandValues = { 'W':0,
                      'A':0,
                      'S':0,
                      'D':0, }

cameraCommandValues = { 'K_UP':0,
                        'K_DOWN':0,
                        'K_LEFT':0,
                        'K_RIGHT':0,
                         }

functionCommandValues = { 'K_SPACE':0,
                          'K_F2':0, }


print ("********\n" + "*READY!*\n" + "********")
print("Press ESCAPE to QUIT")
readytext = myfont.render("READY!", 1, (0,255,0))
screen.blit(readytext, (60, 160))
pygame.draw.circle(screen, (0,255,0), (100,100), 50)
pygame.display.flip()

def checkKeyDown():
    #Change values for Tank Movement
    if event.key == pygame.K_w:
      #print("forward!")
      moveCommandValues['W'] = 1
    if event.key == pygame.K_s:
      #print("reverse")
      moveCommandValues['S'] = 1
    if event.key == pygame.K_a:
      #print("turn left")
      moveCommandValues['A'] = 1
    if event.key == pygame.K_d:
      #print("turn right")
      moveCommandValues['D'] = 1
      robot.stop()

    #Change values for Camera Movement
    if event.key == pygame.K_UP:
      #print("Camera up")
      cameraCommandValues['K_UP'] = 1
    if event.key == pygame.K_DOWN:
      #print("Camera down")
      cameraCommandValues['K_DOWN'] = 1
    if event.key == pygame.K_LEFT:
      #print("Camera left")
      cameraCommandValues['K_LEFT'] = 1
    if event.key == pygame.K_RIGHT:
      #print("Camera right")
      cameraCommandValues['K_RIGHT'] = 1
    if event.key == pygame.K_SPACE:
      functionCommandValues['K_SPACE'] = 1
    if event.key == pygame.K_F2:
      functionCommandValues['K_F2'] = 1


    if event.key == pygame.K_RCTRL:	#Press right CTRL to center PanTilt-kit
      panServo = 365
      tiltServo = 420
      pwm.setPWM(2, 0, panServo)
      pwm.setPWM(3, 0, tiltServo)

    #Press ESCAPE to QUIT
    if event.key == pygame.K_ESCAPE:
      print(moveCommandValues)
      print(cameraCommandValues)
      running = False
      quit()
      pygame.quit()

    else:
        pass

def checkKeyUp():
    #Change values for Tank Movement
    if event.key == pygame.K_w:
      #print("stopFORWARD")
      moveCommandValues['W'] = 0
    if event.key == pygame.K_s:
      #print("stopREVERSE")
      moveCommandValues['S'] = 0
    if event.key == pygame.K_a:
      #print("stopLEFT")
      moveCommandValues['A'] = 0
    if event.key == pygame.K_d:
      #print("stopRIGHT")
      moveCommandValues['D'] = 0

    #Change values for Camera Movement
    if event.key == pygame.K_UP:
      #print("Camera up STOP")
      cameraCommandValues['K_UP'] = 0
    if event.key == pygame.K_DOWN:
      #print("Camera down STOP")
      cameraCommandValues['K_DOWN'] = 0
    if event.key == pygame.K_LEFT:
      #print("Camera left STOP")
      cameraCommandValues['K_LEFT'] = 0
    if event.key == pygame.K_RIGHT:
      #print("Camera right STOP")
      cameraCommandValues['K_RIGHT'] = 0

    if event.key == pygame.K_SPACE:
      functionCommandValues['K_SPACE'] = 0
    if event.key == pygame.K_F2:
      functionCommandValues['K_F2'] = 0

    else:
      pass


while running:
    for event in pygame.event.get():
      #When a key is pressed down
      if event.type == pygame.KEYDOWN:
          checkKeyDown()

      #When a key is released
      if event.type == pygame.KEYUP:
          checkKeyUp()

    #Translate values into movement commands

    #Only forward
    if  moveCommandValues['W'] == 1 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 0:
      robot.RT_forward(speed)
      robot.LT_forward(speed)

    #Left turn while moving forward
    if  moveCommandValues['W'] == 1 \
    and moveCommandValues['A'] == 1 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 0:
      robot.RT_forward(speed)
      robot.LT_forward(reducedSpeed)

    #Right turn while moving forward
    if  moveCommandValues['W'] == 1 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 1:
      robot.RT_forward(reducedSpeed)
      robot.LT_forward(speed)

    #Only reverse
    if  moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 1 \
    and moveCommandValues['D'] == 0:
      robot.RT_backward(speed)
      robot.LT_backward(speed)

    #Left turn while reversing
    if  moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 1 \
    and moveCommandValues['S'] == 1 \
    and moveCommandValues['D'] == 0:
      robot.RT_backward(reducedSpeed)
      robot.LT_backward(speed)

    #Right turn while reversing
    if  moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 1 \
    and moveCommandValues['D'] == 1:
      robot.RT_backward(speed)
      robot.LT_backward(reducedSpeed)

    #Only left turn
    if  moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 1 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 0:
      robot.RT_forward(speed)
      robot.LT_backward(speed)

    #Only right turn
    if  moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 1:
      robot.RT_backward(speed)
      robot.LT_forward(speed)

    #Stop when no keys pressed
    if moveCommandValues['W'] == 0 \
    and moveCommandValues['A'] == 0 \
    and moveCommandValues['S'] == 0 \
    and moveCommandValues['D'] == 0:
      robot.stop()


    #Translate values into camera movement
    if cameraCommandValues['K_UP'] == 1:  #If the key is pressed down
      #print("UP")
      tiltServo -= servoSpeed     #Change the servo position by the value of servoSpeed.
      if tiltServo < tiltMIN:     #If positional value exceeds the set limit,
        tiltServo = tiltMIN       #set it back to its limit value.
      pwm.setPWM(3, 0, tiltServo) #Move the servo to the specified location

    if cameraCommandValues['K_DOWN'] == 1:
      #print("DOWN")
      tiltServo += servoSpeed
      if tiltServo > tiltMAX:
        tiltServo = tiltMAX
      pwm.setPWM(3, 0, tiltServo)

    if cameraCommandValues['K_LEFT'] == 1:
      #print("LEFT")
      panServo += servoSpeed
      if panServo > panMAX:
        panServo = panMAX
      pwm.setPWM(2, 0, panServo)


    if cameraCommandValues['K_RIGHT'] == 1:
      #print("RIGHT")
      panServo -= servoSpeed
      if panServo < panMIN:
        panServo = panMIN
      pwm.setPWM(2, 0, panServo)

    if functionCommandValues['K_SPACE'] == 1: #Laser on
      GPIO.setup(7, GPIO.OUT)
    if functionCommandValues['K_SPACE'] == 0: #Laser off
      GPIO.setup(7, GPIO.IN)

      if functionCommandValues['K_F2'] == 1:
        sonarBot.moveBot()


pygame.quit()
quit()
