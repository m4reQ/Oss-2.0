import pygame
import random
import game
from helper import *
import math

class Circle(object):

	texture_count = 0
	font_textures = []
	radius = 0

	def Load_texture(texPath, texNumber=0):
		texture = pygame.image.load(texPath + '/' + texNumber + '.png')
		texture = pygame.transform.scale(texture, (Circle.radius*2, Circle.radius*2))
		return texture
	
	def __init__(self, surf, X, Y, time, g):
		self.surface = surf
		self.game = g
		self.pos = (X, Y)
		self.is_visible = False
		self.time = time
		self.texture_count = Circle.texture_count

		g = self.game

		if not Circle.font_textures:
			Circle.radius = stats.getCS(g.CS)

			i = 0
			while i < 10:
				texture = Circle.Load_texture('textures/circles', i)
				Circle.font_textures.append(texture)
				i += 1

			if game.DEBUG_MODE:
				print("Initialized textures. Texture array: ")
				print(Circle.font_textures)
		else:
			pass

		if Circle.texture_count < 9:
			Circle.texture_count += 1
		else:
			Circle.texture_count = 0

	def __str__(self):
		rep = "Circle at: " + str(self.pos[0]) + "," + str(self.pos[1]) + ". At time: " + str(self.time)

		return rep
		
	def Draw(self):
		g = self.game

		if g.time == self.time:
			pygame.draw.circle(self.surface, color.green, self.pos, Circle.radius, 2)
			pygame.draw.circle(self.surface, color.gray, self.pos, (Circle.radius + 1), 1)
		else:
			pygame.draw.circle(self.surface, color.white, self.pos, Circle.radius, 2)
			pygame.draw.circle(self.surface, color.gray, self.pos, (Circle.radius + 1), 1)

		font_position = (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius)
		self.surface.blit(Circle.font_textures[self.texture_count], font_position)
		
	def Collide(self):
		"""
		rtype: none
		returns: bool
		"""
		g = self.game

		if g.cursor_pos[0] > (self.pos[0] - Circle.radius) and g.cursor_pos[1] > (self.pos[1] - Circle.radius):
			if g.cursor_pos[0] < (self.pos[0] + Circle.radius) and g.cursor_pos[1] < (self.pos[1] + Circle.radius):
				return True
			else:
				return False

	def Hit(self):
		g = self.game
		
		g.combo += 1
		g.points += (g.combo * 300)
		g.combo_color = color.random()
		if g.combo >= 5:
			g.health += 3
		

	def Miss(self):
		g = self.game

		g.combo = 0
		g.health -= stats.getHP(g.HP) * 100

		# miss_pos = pygame.mouse.get_pos()

		# img = game.miss_texture
		# self.surface.blit(img, (miss_pos[0]-self.radius, miss_pos[1]-self.radius))

if __name__ == '__main__':
	pygame.quit()
	quit()
