import pygame
from launcher import keybind
from launcher import sets

class EventHandler:
	@staticmethod
	def HandleKeys(game, event):
		if event.key == pygame.K_ESCAPE:
			game.is_running = False
			if sets.DEBUG_MODE:
				raise Exception('[INFO] User interruption by closing window')
				
		if event.key == pygame.K_F10:
			game.draw_interface = not game.draw_interface

		#force screen update (ONLY IN DEBUG MODE)
		if sets.DEBUG_MODE:
			if event.key == pygame.K_BACKQUOTE:
				print('[INFO] Preformed window update.')
				pygame.display.update()

		if event.key == keybind['kl']:
			game.click_count[0] += 1
		if event.key == keybind['kr']:
			game.click_count[1] += 1


	@staticmethod
	def HandleEvents(game, event):
		if event.type == pygame.QUIT:
			game.is_running = False
			if sets.DEBUG_MODE:
				raise Exception('[INFO] User interruption by closing window')

if __name__ == '__main__':
	pygame.quit()
	quit()