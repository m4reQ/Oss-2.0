import pygame
import random

radius = 100

#textures load
font_textures = []
i = 0
while i < 10:
	texture = pygame.image.load('textures/circles/' + str(i) + '.png')
	texture = pygame.transform.scale(texture, (radius*2, radius*2))
	font_textures.append(texture)
	i += 1

class Circle(object):

        texture_count = 0
        
	def __init__(self, surf, X, Y, time, texture_count, game):
		self.surface = surf
		self.font_textures = font_textures
		self.radius = radius
		self.game = game
		self.pos = (X, Y)
		self.is_visible = False
		self.time = time

		Circle.texture_count += 1

	def __str__(self):
                rep = "Circle at: " + str(self.pos[0]) + "," + str(self.pos[1]) + ". At time: " + str(self.time)

                return rep
                
	def Draw(self, game):
		g = self.game

		pygame.draw.circle(self.surface, (255,255,255), self.pos, self.radius, 2)
		pygame.draw.circle(self.surface, (128,128,128), self.pos, (self.radius + 1), 1)
		
		if g.texture_count > 9:
			g.health += 10
			g.texture_count = 0

		font_position = (self.pos[0] - self.radius, self.pos[1] - self.radius)
		self.surface.blit(self.font_textures[g.texture_count], font_position)
		
	def Collide(self):
		g = self.game
		
                is_hit = False
		if g.cursor_pos[0] > (self.pos[0] - self.radius) and g.cursor_pos[1] > (self.pos[1] - self.radius):
			if g.cursor_pos[0] < (self.pos[0] + self.radius) and g.cursor_pos[1] < (self.pos[1] + self.radius):
				is_hit = True

		return is_hit

	def Hit(self):
		g = self.game
		
		g.combo += 1
		g.points += (g.combo * 300)
		g.texture_count += 1
		g.combo_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

	def Miss(self):
                g = self.game

                g.combo = 0
                g.health -= 10

                miss_pos = pygame.mouse.get_pos()

                #img = self.miss_texture
                #self.win.blit(img, miss_pos)
