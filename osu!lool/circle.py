import pygame
import random
import game
from helper import *

class Circle():

	texture_count = 0
	font_textures = []
	radius = 0
	
	def __init__(self, X, Y, time=0):
		self.pos = (X, Y)
		self.time = time
		self.texture_count = Circle.texture_count

		if not Circle.font_textures:
			Circle.radius = stats.getCS(game.CS)

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

	@staticmethod
	def Load_texture(texPath, texNumber=0):
		"""
		loads texture to pygame image objects
		rtype: string, int
		returns: pygame.Image
		"""
		texture = pygame.image.load(texPath + '/' + str(texNumber) + '.png')
		texture = pygame.transform.scale(texture, (Circle.radius*2, Circle.radius*2))
		return texture
		
	def Draw(self, surf):
		pygame.draw.circle(surf, color.white, self.pos, Circle.radius, 2)
		pygame.draw.circle(surf, color.gray, self.pos, (Circle.radius + 1), 1)

		font_position = (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius)
		surf.blit(Circle.font_textures[self.texture_count], font_position)
		
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
	        game.combo_color = color.random()
	        if game.combo >= 5:
	        	game.health += stats.getHP(game.HP) * 50

	        game.circles.remove(self)

	def Miss(self, game):
		game.combo = 0
		game.health -= stats.getHP(game.HP) * 100

		game.circles.remove(self)

if __name__ == '__main__':
	pygame.quit()
	quit()
