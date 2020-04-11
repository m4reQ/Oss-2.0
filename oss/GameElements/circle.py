if __name__ == '__main__':
	quit()

import pygame
from utils import stats, color, GetMax
from launcher import CS, HP, AR, scale, CS_raw, HP_raw, AR_raw, mainResManager
from .map import EmptyMap
import math

class Circle(object):
	textureCount = 0
	backgroundCount = 0
	count = 0
	radius = int(CS * scale)

	fadeOutDuration = 0.5 #animation duration in seconds

	def __init__(self, pos, time=0):
		self.pos = pos

		self.destroyed = False
		self.alpha = 255

		if time != -1:
			self.startTime = GetMax(time - AR, 0)
			self.endTime = GetMax(time + AR, 0)
			self.hitTime = GetMax(time - (AR / 2), 0) #a quarter after circle show time
		else:
			self.startTime = -1
			self.endTime = float('inf')
			self.hitTime = float('inf')

		self.textureCount = Circle.textureCount
		self.backgroundCount = Circle.backgroundCount

		self.bgName = 'circlebg_' + str(self.backgroundCount)
		self.fontName = 'circlefont_' + str(self.textureCount)

		self.fontTexture = mainResManager.GetTexture(self.fontName)
		self.bgTexture = mainResManager.GetTexture(self.bgName)

		self.circleSurf = pygame.Surface((Circle.radius * 2 + 4, Circle.radius * 2 + 4), pygame.HWSURFACE | pygame.SRCALPHA)
		self.circleSurf.fill((255, 0, 255))
		self.circleSurf.set_colorkey((255, 0, 255))
		self.circleSurf.blit(self.bgTexture.Get(), (0, 0))
		pygame.draw.circle(self.circleSurf, (255, 255, 255, 255), (int(Circle.radius), int(Circle.radius)), Circle.radius, int(3 * scale))
		pygame.draw.circle(self.circleSurf, (128, 128, 128, 255), (int(Circle.radius), int(Circle.radius)), (Circle.radius + int(1 * scale)), int(1 * scale))
		self.circleSurf.blit(self.fontTexture.Get(), (0, 0))
		self.circleSurf = self.circleSurf.convert()

		if Circle.textureCount < 9:
			Circle.textureCount += 1
		else:
			Circle.textureCount = 0

		if Circle.count % 4 == 0 and Circle.count != 0:
			if Circle.backgroundCount < 4:
				Circle.backgroundCount += 1
			else:
				Circle.backgroundCount = 0

		Circle.count += 1

	def __repr__(self):
		return str('Circle at position: {}. Font texture: {}. Background texture: {}.'.format(self.pos, self.textureCount, self.backgroundCount))
		
	def Draw(self, surf, time):
		if time >= self.startTime and time <= self.endTime:
			self.circleSurf.set_alpha(self.alpha)
			surf.blit(self.circleSurf, (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))
			if time >= self.hitTime and time <= self.endTime:
				if not self.destroyed:
					surf.blit(mainResManager.GetTexture("hitlayout").Get(), (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius))

	def Update(self, game):
		if self.destroyed:
			self.alpha -= 255 / 0.5 * game.frameTime #int(255.0 / Circle.fadeOutDuration * (1 / game.frameTime))

		if self.alpha <= 0:
			game.map.objectsLeft.remove(self)
	
	def Collide(self, game, cursor_pos):
		"""
		checks if clicked point is inside a circle
		rtype: tuple
		returns: bool
		"""
		if math.sqrt((self.pos[0] - cursor_pos[0])**2 + (self.pos[1] - cursor_pos[1])**2) <= self.radius:
			self.Hit(game)
		else:
			self.Miss(game)

	def Hit(self, game):
		if self.destroyed:
			return

		if game.combo % 5 == 0 and game.combo != 0:
			mainResManager.GetSound('hit2').Play()
		else:
			mainResManager.GetSound('hit1').Play()

		game.combo += 1

		if self.startTime < 0:
			scoredPoints = stats.CalculatePoints(game.combo, 1, CS_raw, HP_raw)
		else:
			scoredPoints = stats.CalculatePoints(game.combo, AR_raw, CS_raw, HP_raw)

		if self.startTime < -1:
			game.points += scoredPoints
		elif game.time_ms >= self.startTime and game.time_ms <= self.hitTime:
			game.points += int(scoredPoints / 2)
		elif game.time_ms >= self.hitTime:
			game.points += scoredPoints

		game.pointsColor = color.random()

		if game.combo >= 5:
			game.health += HP * 50

		if isinstance(game.map, EmptyMap):
			game.GenerateRandomCircle()
		self.destroyed = True
		
	def Miss(self, game):
		if self.destroyed:
			return

		mainResManager.GetSound('miss').Play()

		game.combo = 0
		game.health -= HP * 100
		game.pointsColor = color.random()

		if isinstance(game.map, EmptyMap):
			game.GenerateRandomCircle()
		self.destroyed = True