if __name__ == '__main__':
	import sys
	sys.exit()

import pygame
from launcher import debugging, prefs

class EventHandler:
	@staticmethod
	def HandleKeys(game, event):
		if event.key == pygame.K_ESCAPE:
			game.isRunning = False
			if debugging:
				print('[INFO]<{}> User interruption by closing window'.format(__name__))
				
		if event.key == prefs.keyBinds['hideInterface']:
			game.draw_interface = not game.draw_interface

		#force screen update (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == prefs.keyBinds['debugUpdateWindow']:
				print('[INFO]<{}> Preformed window update.'.format(__name__))
				pygame.display.update()
		
		#get current mouse position (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == prefs.keyBinds['debugGetPos']:
				pos = pygame.mouse.get_pos()
				print('[INFO]<{}> Current mouse position: {}, mapped coords (current resolution): {}'.format(__name__, pos, (pos[0] / game.width, pos[1] / game.height)))

		try: #try to increment click_count
			if event.key == prefs.keyBinds['kl']:
				game.click_count[0] += 1
			if event.key == prefs.keyBinds['kr']:
				game.click_count[1] += 1
		except AttributeError: #if it's not there and we're in menu pass
			pass

	@staticmethod
	def HandleMouse(game, event):
		try:
			if event.button == 1:
				game.click_count[0] += 1
			elif event.button == 3:
				game.click_count[1] += 1
		except AttributeError:
			pass

	@staticmethod
	def HandleEvents(game, event):
		if event.type == pygame.QUIT:
			game.isRunning = False
			if debugging:
				print('[INFO]<{}> User interruption by closing window.'.format(__name__))

	@staticmethod
	def HandleInternalEvents(game):
		if game.health <= 0:
			if debugging:
				print('[INFO]<{}> Health reached {}.'.format(__name__, game.health))
			game.isRunning = False

		if game.health >= game.maxhealth:
			game.health = game.maxhealth

		if game.time_ms >= game.map.length:
			game.map.shouldPlay = False

		if not game.map.shouldPlay:
			if debugging:
				print('[INFO]<{}> Map ended at time: {}ms.'.format(__name__, game.time))
			game.isRunning = False