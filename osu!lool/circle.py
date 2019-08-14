import pygame
import random
import game

class Circle(object):

	texture_count = 0
	font_textures = []
	
	def __init__(self, surf, X, Y, time, g):
		self.surface = surf
		self.game = g
		self.pos = (X, Y)
		self.is_visible = False
		self.time = time
		self.texture_count = Circle.texture_count

		Circle.texture_count += 1

		if not Circle.font_textures:
			Circle.radius = 150/game.CS
			
			i = 0
			while i < 10:
				texture = pygame.image.load('textures/circles/' + str(i) + '.png')
				texture = pygame.transform.scale(texture, (Circle.radius*2, Circle.radius*2))
				Circle.font_textures.append(texture)
				i += 1

			if game.DEBUG_MODE:
				print("Initialized textures. Texture array: ")
				print(Circle.font_textures)
		else:
			pass

	def __str__(self):
		rep = "Circle at: " + str(self.pos[0]) + "," + str(self.pos[1]) + ". At time: " + str(self.time)

		return rep
		
	def Draw(self):
		g = self.game

		pygame.draw.circle(self.surface, (255,255,255), self.pos, Circle.radius, 2)
		pygame.draw.circle(self.surface, (128,128,128), self.pos, (Circle.radius + 1), 1)
			
		if Circle.texture_count > 9:
			g.health += 10
			Circle.texture_count = 0

		font_position = (self.pos[0] - Circle.radius, self.pos[1] - Circle.radius)
		self.surface.blit(self.font_textures[self.texture_count], font_position)
		
	def Collide(self):
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
