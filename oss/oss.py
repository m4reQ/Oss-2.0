import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
from helper import logError, exitAll
import launcher

try:
	if __name__ == '__main__':
		launcher.Start()
	else:
		raise Exception('[ERROR] Tried to access main launch method from external module.')
except Exception as e:
	logError(e)
	print(e)

	exitAll()