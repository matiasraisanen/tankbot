import pygame
import os
import Robot
import threading

speed = 100
robot = Robot.Robot(left_trim=0, right_trim=0)

#os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
screen = pygame.display.set_mode((10, 10)) 

gameExit = False

commandValues = {'W':0,
                 'A':0,
                 'S':0,
                 'D':0,}

print ("ready!")
while not gameExit:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          print("forward!")
          commandValues['W'] = 1
        if event.key == pygame.K_s:
          print("reverse")
          commandValues['S'] = 1
        if event.key == pygame.K_a:
          print("turn left")
          commandValues['A']= 1
        if event.key == pygame.K_d:
          print("turn right")
          commandValues['D'] = 1
        
        if event.key == pygame.K_q:
          print(commandValues)
          gameExit = True
        if event.key == pygame.K_SPACE:
          print("stop")
          robot.stop()

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          print("stopFORWARD")
          commandValues['W'] = 0
        if event.key == pygame.K_s:
          print("stopREVERSE")
          commandValues['S'] = 0
        if event.key == pygame.K_a:
          print("stopLEFT")
          commandValues['A'] = 0
        if event.key == pygame.K_d:
          print("stopRIGHT")
          commandValues['D'] = 0

    if commandValues['W'] == 1:
      robot.RT_forward(speed)
      robot.LT_forward(speed)
    if commandValues['S'] == 1:
      robot.RT_backward(speed)
      robot.LT_backward(speed)
    if commandValues['A'] == 1:
      robot.RT_forward(speed)
      robot.LT_backward(speed)
    if commandValues['D'] == 1:
      robot.RT_backward(speed)
      robot.LT_forward(speed)

pygame.quit()
quit()