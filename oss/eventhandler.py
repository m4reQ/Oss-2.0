if __name__ == '__main__':
	quit()

import pygame

debugging = False

keyBindTable = {
	'quit': pygame.K_ESCAPE,
	'kl': pygame.K_z,
	'kr': pygame.K_x,
	'updateWindow': pygame.K_BACKQUOTE,
	'hideInterface': pygame.K_F10,
	'debugGetPos': pygame.K_F1
}

def SetDebugging(val):
	"""
	sets debugging mode to given value
	rtype: bool
	returns: None
	"""
	global debugging
	debugging = val

def BindKeys(keybind):
	"""
	sets key table to given value
	rtype: Dictionary<string, pygame.event.key>
	returns: None
	"""
	global keyBindTable
	for key, value in keybind:
		keyBindTable[key] = value

def BindKey(keyName, keyAssignment):
	"""
	binds certain key from key table
	rtype: string, pygame.event.key
	returns: None
	"""
	global keyBindTable
	keyBindTable[keyName] = keyAssignment

class EventHandler:
	@staticmethod
	def HandleKeys(game, event):
		if event.key == keyBindTable['quit']:
			game.isRunning = False
			if debugging:
				print('[INFO]<{}> User interruption by closing window'.format(__name__))
				
		if event.key == keyBindTable['hideInterface']:
			game.draw_interface = not game.draw_interface

		#force screen update (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == keyBindTable['updateWindow']:
				print('[INFO]<{}> Preformed window update.'.format(__name__))
				pygame.display.update()
		
		#get current mouse position (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == keyBindTable['debugGetPos']:
				pos = pygame.mouse.get_pos()
				print('[INFO]<{}> Current mouse position: {}, mapped coords (current resolution): {}'.format(__name__, pos, (pos[0] / game.width, pos[1] / game.height)))

		try: #try to increment click_count
			if event.key == keyBindTable['kl']:
				game.click_count[0] += 1
			if event.key == keyBindTable['kr']:
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
				print('[INFO]<{}> health reached {}.'.format(__name__, game.health))
			game.isRunning = False

		if game.health >= game.maxhealth:
			game.health = game.maxhealth

		if game.time_ms >= game.map.length:
			game.map.shouldPlay = False

		if not game.map.shouldPlay:
			if debugging:
				print('[INFO]<{}> Map ended at time: {}ms.'.format(__name__, game.time))
			game.isRunning = False