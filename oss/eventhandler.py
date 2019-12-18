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
			game.is_running = False
			if debugging:
				print('[INFO]<', str(__name__), '> User interruption by closing window')
				
		if event.key == keyBindTable['hideInterface']:
			game.draw_interface = not game.draw_interface

		#force screen update (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == keyBindTable['updateWindow']:
				print('[INFO]<', str(__name__), '> Preformed window update.')
				pygame.display.update()
		
		#get current mouse position (ONLY IN DEBUG MODE)
		if debugging:
			if event.key == keyBindTable['debugGetPos']:
				pos = pygame.mouse.get_pos()
				print('[INFO]<', str(__name__), '> Current mouse position: ', pos, ', mapped coords (current resolution): ', str(pos[0] / game.width), str(pos[1] / game.height))

		if event.key == keyBindTable['kl']:
			game.click_count[0] += 1
		if event.key == keyBindTable['kr']:
			game.click_count[1] += 1

	@staticmethod
	def HandleEvents(game, event):
		if event.type == pygame.QUIT:
			game.is_running = False
			if debugging:
				print('[INFO]<', str(__name__), '> User interruption by closing window')

	@staticmethod
	def HandleInternalEvents(game):
		if game.health <= 0:
			if debugging:
				print('[INFO]<', str(__name__), '> health reached ' + str(game.health))
			game.is_running = False

		if game.health >= game.maxhealth:
			game.health = game.maxhealth

		if not game.circles:
			if debugging:
				print('[INFO]<', str(__name__), '> List depleted at time: ', str(game.time), 'ms.')
			game.is_running = False

if __name__ == '__main__':
	pygame.quit()
	quit()