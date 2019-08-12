import pygame
import random
import game

while True:
        if game.Check_response():
                break

radius = game.CS
radius = 150/radius

#textures loading
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
		self.texture_count = Circle.texture_count

		Circle.texture_count += 1

	def __str__(self):
		rep = "Circle at: " + str(self.pos[0]) + "," + str(self.pos[1]) + ". At time: " + str(self.time)

		return rep
		
	def Draw(self):
		g = self.game

		pygame.draw.circle(self.surface, (255,255,255), self.pos, self.radius, 2)
		pygame.draw.circle(self.surface, (128,128,128), self.pos, (self.radius + 1), 1)
			
		if Circle.texture_count > 9:
			g.health += 10
			Circle.texture_count = 0

		font_position = (self.pos[0] - self.radius, self.pos[1] - self.radius)
		self.surface.blit(self.font_textures[self.texture_count], font_position)
		
	def Collide(self):
		g = self.game

		if g.cursor_pos[0] > (self.pos[0] - self.radius) and g.cursor_pos[1] > (self.pos[1] - self.radius):
			if g.cursor_pos[0] < (self.pos[0] + self.radius) and g.cursor_pos[1] < (self.pos[1] + self.radius):
				return True
			else:
				return False

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

		#img = g.miss_texture
		#self.surface.blit(img, (miss_pos[0]-self.radius, miss_pos[1]-self.radius))

if __name__ == '__main__':
	pygame.quit()
	quit()
