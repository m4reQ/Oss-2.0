import pygame
import random

pygame.init()

class Circle(object):
	def __init__(self, surf, X, Y, texture_count):
		self.x = X
		self.y = Y
		self.to_click = False
		self.surface = surf
		self.font_texture = None
		self.radius = 30

	def Click(self, game, circle):
		g = game
		g.texture_count += 1
		g.combo += 1
		g.points += (g.combo * 300)
		g.circles.remove(circle)
		g.Generate_circle(g.texture_count)
		g.combo_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


	def Draw(self, game):
		g = game
		pos = (self.x, self.y)
		pygame.draw.circle(self.surface, (255,255,255), pos, self.radius, 2)
		pygame.draw.circle(self.surface, (128,128,128), pos, (self.radius + 1), 1)
		if g.texture_count > 9:
			g.texture_count = 0

		self.font_texture = pygame.image.load('textures/circles/' + str(g.texture_count) + '.png')
		self.font_texture = pygame.transform.scale(self.font_texture, (self.radius*2, self.radius*2))
		font_position = (pos[0] - self.radius, pos[1] - self.radius)
		self.surface.blit(self.font_texture, font_position)
		
