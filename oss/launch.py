try:
	import os
	import sys
except ImportError:
	print('Critical error! Cannot load os or sys module.')
	os.system('pause >NUL')
	exit()

try:
	ext_modules = ['pygame', 'itertools']
	os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
	import repair
	import game
	from game import TEST_MODE, DEBUG_MODE
	from helper import ask, logError
	import update
	import pygame
	import pygame.locals
except ImportError as e:
	logError(e)
	print('Error! One of modules cannot be resolved. \nTry restarting your application or reinstalling it.')

	if repair.Check_response():
		if ask("Do you want to launch the repair module?"):
			repair.main(ext_modules)

	print('Module checking done.')

	os.system('pause >NUL')
	quit()

if __name__ == '__main__':
	try:
		if TEST_MODE:
			raise Exception('[INFO] Test mode enabled.')

		if not DEBUG_MODE:
			update.Check_version()
	
		g = game.Game(game.resolution)

		g.Run()

	except Exception as e:
		logError(e)
		print(e)

	pygame.quit()
	os.system("pause >NUL")
	quit()