import vgamepad as vg
from time import sleep

gamepad = vg.VX360Gamepad()

while 1:
	gamepad.left_joystick_float(x_value_float = -1, y_value_float = 0.0)
	gamepad.update()
	sleep(0.5)
	gamepad.left_joystick_float(x_value_float = 1, y_value_float = 0.0)
	gamepad.update()
	sleep(0.5)