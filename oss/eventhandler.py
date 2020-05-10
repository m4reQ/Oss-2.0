if __name__ == '__main__':
	import sys
	sys.exit()

import pygame
from launcher import debugging, prefs

class EventHandler:
	def __init__(self, game):
		self.game = game

	def HandleKeys(self, event):
		if event.key == pygame.K_ESCAPE:
			self.game.isRunning = False
			if debugging:
				print('[INFO]<{}> User interruption by closing window'.format(__name__))
				
		if event.key == prefs.keyBinds['hideInterface']:
			self.game.draw_interface = not self.game.draw_interface

		if debugging:
			#force screen update
			if event.key == prefs.keyBinds['debugUpdateWindow']:
				print('[INFO]<{}> Preformed window update.'.format(__name__))
				pygame.display.update()
			
			#get current mouse position
			if event.key == prefs.keyBinds['debugGetPos']:
				pos = pygame.mouse.get_pos()
				print('[INFO]<{}> Current mouse position: {}, mapped coords (current resolution): {}'.format(__name__, pos, (pos[0] / self.game.width, pos[1] / self.game.height)))
			
			#toggle profiling
			if event.key == prefs.keyBinds['debugProfile']:
				self.game.profiling = not self.game.profiling
		
		try: #try to increment click_count
			if event.key == prefs.keyBinds['kl']:
				self.game.click_count[0] += 1
			if event.key == prefs.keyBinds['kr']:
				self.game.click_count[1] += 1
		except AttributeError: #if it's not there and we're in menu pass
			pass

	def HandleMouse(self, event):
		try:
			if event.button == 1:
				self.game.click_count[0] += 1
			elif event.button == 3:
				self.game.click_count[1] += 1
		except AttributeError:
			pass

	def HandleEvents(self, event):
		if event.type == pygame.QUIT:
			self.game.isRunning = False
			if debugging:
				print('[INFO]<{}> User interruption by closing window.'.format(__name__))

	def HandleInternalEvents(self):
		if self.game.health <= 0:
			if debugging:
				print('[INFO]<{}> Health reached {}.'.format(__name__, self.game.health))
			self.game.isRunning = False

		if self.game.health >= self.game.maxHealth:
			self.game.health = self.game.maxHealth

		if self.game.time_ms >= self.game.map.length:
			self.game.map.shouldPlay = False

		if not self.game.map.shouldPlay:
			if debugging:
				print('[INFO]<{}> Map ended at time: {}ms.'.format(__name__, self.game.time))
			self.game.isRunning = False