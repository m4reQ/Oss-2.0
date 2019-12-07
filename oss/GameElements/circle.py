import pygame
from game import DEBUG_MODE
from helper import *
from launcher import circleTextures as TextureContainer
from launcher import CS, HP
from launcher import scale
import math

class Circle(object):
	texture_count = 0
	background_count = 0
	count = 0
	radius = int(stats.getCS(CS) * scale)

	def __init__(self, X, Y, time=0):

		self.pos = (X, Y)
		self.time = time

		self.texture_count = Circle.texture_count
		self.background_count = Circle.background_count

		self.font_name = str('font_' + str(self.texture_count))
		self.bg_name = str('bg_' + str(self.background_count))

		if Circle.texture_count < 9:
			Circle.texture_count += 1
		else:
			Circle.texture_count = 0

		if Circle.count % 4 == 0:
			if Circle.background_count < 4:
				Circle.background_count += 1
			else:
				Circle.background_count = 0

		Circle.count += 1

	def __repr__(self):
		return str('Circle at position: ' + str(self.pos) + '. Font texture: ' + self.font_name + '. Background texture: ' + self.bg_name + '.')
		
	def Draw(self, surf):
		surf.blit(TextureContainer.GetTexture(self.bg_name), (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))

		pygame.draw.circle(surf, color.white, self.pos, Circle.radius, int(2 * scale))
		pygame.draw.circle(surf, color.gray, self.pos, (Circle.radius + int(1 * scale)), int(1 * scale))

		font_position = (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius)
		surf.blit(TextureContainer.GetTexture(self.font_name), font_position)
		
	def Collide(self, cursor_pos):
		"""
		checks if clicked point is inside a circle
		rtype: tuple
		returns: bool
		"""
		dist = math.sqrt((self.pos[0] - cursor_pos[0])**2 + (self.pos[1] - cursor_pos[1])**2)
		return dist <= self.radius

	def Hit(self, game):
		game.combo += 1
		game.points += (game.combo * 300)
		game.points_text.textColor = color.random()
		if game.combo >= 5:
			game.health += stats.getHP(HP) * 50

		game.circles.remove(self)
		
	def Miss(self, game):
		game.combo = 0
		game.health -= stats.getHP(HP) * 100

		game.circles.remove(self)

if __name__ == '__main__':
	pygame.quit()
	quit()
