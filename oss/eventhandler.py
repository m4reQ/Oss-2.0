import pygame
import pygame.locals

class EventHandler:
	@staticmethod
	def HandleKeys(game, event, debug_mode=False):
		if event.key == pygame.K_ESCAPE:
			game.is_running = False
			if debug_mode:
				raise Exception('[INFO] User interruption by closing window')
				
		if event.key == pygame.K_F10:
			game.draw_interface = not game.draw_interface

		#force screen update (ONLY IN DEBUG MODE)
		if debug_mode:
			if event.key == pygame.K_BACKQUOTE:
				print('[INFO] Preformed window update.')
				pygame.display.update()

		if event.key == pygame.K_z:
			game.click_count[0] += 1
		if event.key == pygame.K_x:
			game.click_count[1] += 1


	@staticmethod
	def HandleEvents(game, event, debug_mode=False):
		if event.type == pygame.QUIT:
			game.is_running = False
			if debug_mode:
				raise Exception('[INFO] User interruption by closing window')

if __name__ == '__main__':
	pygame.quit()
	quit()