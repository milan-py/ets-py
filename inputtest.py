import pygame
from pygame.locals import *


pygame.joystick.init()
pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]


while 1:
    for event in pygame.event.get():
        if event.type == JOYBUTTONUP:
            print(f"Button: {event.button}")
        if event.type == JOYAXISMOTION:
            print(f"axis: {event.axis} value: {event.value} id: {event.instance_id}")