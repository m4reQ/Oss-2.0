import pygame
from game import scale as scale
import game
from helper import *
import math

class Circle():
	texture_count = 0
	background_count = 0
	count = 0
	font_textures = []
	background_textures = []
	radius = int(stats.getCS(game.CS) * scale)

	def __init__(self, X, Y, time=0):
		self.pos = (X, Y)
		self.time = time
		self.texture_count = Circle.texture_count
		self.background_count = Circle.background_count

		#check if textures was previously loaded
		#this should happen only once on the first circle generation
		if not Circle.font_textures and not Circle.background_textures:
			#load font textures
			for i in range(10):
				texture = Circle.LoadFontTexture('textures/circles', i)
				Circle.font_textures.append(texture)
			#load background textures
			for i in range(5):
				texture = Circle.LoadBackgroundTexture('textures/circles', i)
				Circle.background_textures.append(texture)

			if game.DEBUG_MODE:
				print("Initialized textures. Texture arrays: ")
				print(Circle.font_textures)
				print(Circle.background_textures)
		else:
			pass

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
		return str('Circle at position: ' + str(self.pos))

	@staticmethod
	def LoadFontTexture(texPath, texNumber=0):
		"""
		loads font texture to pygame image objects
		rtype: string, int
		returns: pygame.Image
		"""
		texture = pygame.image.load(texPath + '/' + str(texNumber) + '.png')
		texture = pygame.transform.scale(texture, (Circle.radius*2, Circle.radius*2))
		return texture

	@staticmethod
	def LoadBackgroundTexture(texPath, texNumber=0):
		"""
		loads circle background texture to pygame image objects
		rtype: string, int
		returns: pygame.Image
		"""
		texture = pygame.image.load(texPath + '/' + 'circlebg_' + str(texNumber) + '.png')
		texture = pygame.transform.scale(texture, (Circle.radius*2, Circle.radius*2))

		return texture
		
	def Draw(self, surf):
		surf.blit(Circle.background_textures[self.background_count], (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))
		pygame.draw.circle(surf, color.white, self.pos, Circle.radius, int(2 * scale))
		pygame.draw.circle(surf, color.gray, self.pos, (Circle.radius + int(1 * scale)), int(1 * scale))

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
