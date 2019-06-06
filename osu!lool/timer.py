import pygame

pygame.init()

class Timer():
	def __init__(self, tick):
		self.time = 0
		self.tick = tick
		self.clock = pygame.time.Clock()

	def Tick(self):
		pygame.display.update()
		self.time += 1
		self.clock.tick(self.tick)

	def Change_tick_rate(self):
		self.tick += 1