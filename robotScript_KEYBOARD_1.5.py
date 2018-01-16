#This script allows you control the tank with WASD
#Keys can be held down
import pygame
from pygame.locals import *
import os
import Robot

speed = 100
robot = Robot.Robot(left_trim=0, right_trim=0)

#os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
screen = pygame.display.set_mode((100, 100)) 

gameExit = False
print("Ready!")

while not gameExit:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          print("forward!")
          robot.RT_forward(speed)
          robot.LT_forward(speed)
        if event.key == pygame.K_s:
          print("reverse")
          robot.RT_backward(speed)
          robot.LT_backward(speed)
        if event.key == pygame.K_a:
          print("turn left")
          robot.RT_forward(speed)
          robot.LT_backward(speed)
        if event.key == pygame.K_d:
          print("turn right")
          robot.RT_backward(speed)
          robot.LT_forward(speed)
        
        if event.key == pygame.K_q:
          print("Quit")
          gameExit = True
        if event.key == pygame.K_SPACE:
          print("stop")
          robot.stop()

      if event.type == pygame.KEYUP:
        if event.key == pygame.K_w:
          print("stop")
          robot.stop()
        if event.key == pygame.K_s:
          print("stop")
          robot.stop()
        if event.key == pygame.K_a:
          print("stop")
          robot.stop()
        if event.key == pygame.K_d:
          print("stop")
          robot.stop()
pygame.quit()
quit()
