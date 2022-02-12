import pygame
from pygame.locals import *

import vgamepad as vg

from PIL import Image, ImageGrab
from time import sleep

import winsound

gamepad = vg.VX360Gamepad()


pygame.joystick.init()
pygame.init()

joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]



RIGHT = 7
LEFT = 6
TOGGLEAUTO = 2
STEERINGAXIS = 0

value = 0
previousvalue = 0
auto = False
lanes = [85, 98]
lane = 0
correction = lanes[0]

previous_auto_toggle = False

warning_given = False

while 1:
	screenshot = ImageGrab.grab(bbox = (2150, 1100, 2350, 1200))
	for i in range(150):
		if screenshot.getpixel((i, 10))[0] > 200 and screenshot.getpixel((i, 10))[1] < 30 and screenshot.getpixel((i, 10))[1] < 30:
			# print(f"index: {i}, color: {screenshot.getpixel((i, 10))}")
			break
	
	toggled = False
	
	for event in pygame.event.get():
		if event.type == JOYAXISMOTION and event.axis == STEERINGAXIS:
			value = event.value
			if(previousvalue < -0.5 and value == 1):
				value = -value
			
			previousvalue = value
		elif event.type == JOYBUTTONUP:
			if event.button == RIGHT:
				lane = 0
			elif event.button == LEFT:
				lane = 1
			elif event.button == TOGGLEAUTO:
				if not previous_auto_toggle:
					if auto:
						auto = False
						winsound.PlaySound("aus.wav", winsound.SND_ASYNC)

					else:
						auto = True
						winsound.PlaySound("an.wav", winsound.SND_ASYNC)

		
		if event.type == JOYBUTTONUP and event.button == TOGGLEAUTO:
			previous_auto_toggle = True
			toggled = True
		elif not toggled: 
			previous_auto_toggle = False



	if lane == 0:
		if correction < lanes[0]+1:correction = lanes[0]
		else:correction -= 0.25

	if lane == 1:
		if correction > lanes[1]-1: correction = lanes[1]
		else: correction += 0.25

	print(f"correction {correction}, lane {lane}")

	if auto:
		if(abs(value) > 0.1):
			auto = False
			winsound.PlaySound("aus.wav", winsound.SND_ASYNC)
		if i != 149:
			i = (i - correction)/200
			gamepad.left_joystick_float(x_value_float = i, y_value_float = 0.0)
			gamepad.update()
			warning_given = False
		else:
			if not warning_given:
				winsound.PlaySound("fehler.wav", winsound.SND_ASYNC)
				warning_given = True
				
			gamepad.left_joystick_float(x_value_float = value*value if value > 0 else -(value*value), y_value_float = 0.0)
			gamepad.update()
	else:
		gamepad.left_joystick_float(x_value_float = value*value if value > 0 else -(value*value), y_value_float = 0.0)
		gamepad.update()
		lane = 0
