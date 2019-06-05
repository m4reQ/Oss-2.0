import pygame

pygame.init()

class Timer():
	def __init__(self, tick):
		self.tick = tick
		self.clock = pygame.time.Clock()

	def Tick(self):
		pygame.display.flip()
		self.clock.tick(self.tick)

	def Change_tick_rate(self):
		self.tick += 1