import pygame
from utils import stats, color
from launcher import circleTextures as TextureContainer
from launcher import hitsounds as SoundContainer
from launcher import CS, HP, AR, scale
import math

class Circle(object):
	texture_count = 0
	background_count = 0
	count = 0
	radius = int(CS * scale)

	def __init__(self, X, Y, time=0):

		self.pos = (X, Y)

		self.startTime = time - AR
		self.endTime = time + AR
		self.hitTime = time - (AR / 2) #a quarter after circle show time

		self.texture_count = Circle.texture_count
		self.background_count = Circle.background_count

		self.font_name = 'font_{}'.format(self.texture_count)
		self.bg_name = 'bg_{}'.format(self.background_count)

		self.animationCount = 0

		if Circle.texture_count < 9:
			Circle.texture_count += 1
		else:
			Circle.texture_count = 0

		if Circle.count % 4 == 0 and Circle.count != 0:
			if Circle.background_count < 4:
				Circle.background_count += 1
			else:
				Circle.background_count = 0

		Circle.count += 1

	def __repr__(self):
		return str('Circle at position: {}. Font texture: {}. Background texture: {}.'.format(self.pos, self.font_name, self.bg_name))
		
	def Draw(self, surf):
		if self.animationCount < 256: self.animationCount += 1

		surf.blit(TextureContainer.GetTexture(self.bg_name), (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))

		pygame.draw.circle(surf, (color.white[0], color.white[1], color.white[2], self.animationCount), self.pos, Circle.radius, int(3 * scale))
		pygame.draw.circle(surf, (color.gray[0], color.gray[1], color.gray[2], self.animationCount), self.pos, (Circle.radius + int(1 * scale)), int(1 * scale))

		surf.blit(TextureContainer.GetTexture(self.font_name), (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))
	
	def DrawLayout(self, surf):
		surf.blit(TextureContainer.GetTexture("hitlayout"), (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))
		
	def Collide(self, game, cursor_pos):
		"""
		checks if clicked point is inside a circle
		rtype: tuple
		returns: bool
		"""
		dist = math.sqrt((self.pos[0] - cursor_pos[0])**2 + (self.pos[1] - cursor_pos[1])**2)
		if dist <= self.radius:
			self.Hit(game)
		else:
			self.Miss(game)

	def Hit(self, game):
		if game.combo % 5 == 0 and game.combo != 0:
			SoundContainer.GetSound('hit2').play()
		else:
			SoundContainer.GetSound('hit1').play()

		game.combo += 1

		scoredPoints = stats.getScoredPoints(game.combo)

		if game.time == -1:
			game.points += scoredPoints
		elif game.time >= self.startTime and game.time <= self.hitTime:
			game.points += int(scoredPoints / 2)
		elif game.time >= self.hitTime:
			game.points += scoredPoints

		game.points_text.textColor = color.random()

		if game.combo >= 5:
			game.health += HP * 50

		game.circles.remove(self)
		
	def Miss(self, game):
		SoundContainer.GetSound('miss').play()

		game.combo = 0
		game.health -= HP * 100
		game.points_text.textColor = color.random()

		game.circles.remove(self)

if __name__ == '__main__':
	pygame.quit()
	quit()
