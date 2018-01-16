#Improved KEYBOARD control with WASD.
#FORWARD plus TURN results in a slow turn.
#TURN results in faster turn.
#Keys can be held down

import pygame
import os, sys
import Robot
import threading

speed = 255	#Speed multiplier, values 0-255
robot = Robot.Robot(left_trim=0, right_trim=0)

#os.environ['SDL_VIDEODRIVER'] = 'dummy'
pygame.init()
screen = pygame.display.set_mode((100, 100)) 

running = True

#Dictionary for command values.
moveCommandValues = { 'W':0,
                      'A':0,
                      'S':0,
                      'D':0, }

cameraCommandValues = { 'K_UP':0,
                        'K_DOWN':0,
                        'K_LEFT':0,
                        'K_RIGHT':0, }

print ("ready!")
while running:
    for event in pygame.event.get():
      #When a key is pressed down
      if event.type == pygame.KEYDOWN:

        #Change values for Tank Movement
        if event.key == pygame.K_w:
          print("forward!")
          moveCommandValues['W'] = 1
        if event.key == pygame.K_s:
          print("reverse")
          moveCommandValues['S'] = 1
        if event.key == pygame.K_a:
          print("turn left")
          moveCommandValues['A']= 1
        if event.key == pygame.K_d:
          print("turn right")
          moveCommandValues['D'] = 1
        if event.key == pygame.K_SPACE:
          print("stop")
          robot.stop()
        
        #Change values for Camera Movement
        if event.key == pygame.K_UP:
          print("Camera up")
          cameraCommandValues['K_UP'] = 1
        if event.key == pygame.K_DOWN:
          print("Camera down")
          cameraCommandValues['K_DOWN'] = 1
        if event.key == pygame.K_LEFT:
          print("Camera left")
          cameraCommandValues['K_LEFT'] = 1
        if event.key == pygame.K_RIGHT:
          print("Camera right")
          cameraCommandValues['K_RIGHT'] = 1
  
        #Press ESCAPE to QUIT
        if event.key == pygame.K_ESCAPE:
          print(moveCommandValues)
          print(cameraCommandValues)
          running = False

      #When a key is released
      if event.type == pygame.KEYUP:
        
        #Change values for Tank Movement
        if event.key == pygame.K_w:
          print("stopFORWARD")
          moveCommandValues['W'] = 0
        if event.key == pygame.K_s:
          print("stopREVERSE")
          moveCommandValues['S'] = 0
        if event.key == pygame.K_a:
          print("stopLEFT")
          moveCommandValues['A'] = 0
        if event.key == pygame.K_d:
          print("stopRIGHT")
          moveCommandValues['D'] = 0

        #Change values for Camera Movement
        if event.key == pygame.K_UP:
          print("Camera up STOP")
          cameraCommandValues['K_UP'] = 0
        if event.key == pygame.K_DOWN:
          print("Camera down STOP")
          cameraCommandValues['K_DOWN'] = 0
        if event.key == pygame.K_LEFT:
          print("Camera left STOP")
          cameraCommandValues['K_LEFT'] = 0
        if event.key == pygame.K_RIGHT:
          print("Camera right STOP")
          cameraCommandValues['K_RIGHT'] = 0

    #Translate values into movement commands
    if moveCommandValues['W'] == 1:
      robot.RT_forward(speed)
      robot.LT_forward(speed)
    if moveCommandValues['S'] == 1:
      robot.RT_backward(speed)
      robot.LT_backward(speed)
    if moveCommandValues['A'] == 1:
      robot.RT_forward(speed)
      robot.LT_backward(speed)
    if moveCommandValues['D'] == 1:
      robot.RT_backward(speed)
      robot.LT_forward(speed)
    if moveCommandValues['W'] == 0 and moveCommandValues['A'] == 0 and
       moveCommandValues['S'] == 0 and moveCommandValues['D'] == 0:
      robot.stop()


pygame.quit()
quit()
