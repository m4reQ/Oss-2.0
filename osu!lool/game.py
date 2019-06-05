import pygame
import circle, timer
import random

pygame.init()

width = 1280
height = 720

#load textures
cursor_texture = pygame.image.load('textures/cursor.png')
cursor_texture = pygame.transform.scale(cursor_texture, (16, 16))
miss_texture = pygame.image.load('textures/miss.png')

pygame.mouse.set_visible(False)

class Game():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.win = pygame.display.set_mode((width, height))
		self.is_running = True
		self.circles = []
		self.click_count = 0
		self.cursor_pos = (0, 0)
		self.playfield = (self.width - (self.width/10), self.height - (self.height/10))
		self.points = 0
		self.combo = 0
		self.combo_color = (255, 255, 255)
		self.texture_count = 0
		self.cursor_texture = cursor_texture
		self.miss_texture = miss_texture
		self.font = pygame.font.SysFont("comicsansms", 48)
		self.maxhealth = 100
		self.health = self.maxhealth

	def Run(self):
		self.Generate_circle(self.texture_count)
		while self.is_running:
			for event in pygame.event.get():
				self.Draw(event)
				self.HealthBar()
				self.Combo()
				self.Cursor()

				if event.type == pygame.QUIT:
					self.is_running = False

				if self.health <= 0:
					self.is_running = False

			Timer.Tick()

	def Draw(self, event):
		for circle in self.circles:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_z or event.key == pygame.K_x:
					if self.Collide(circle):
						circle.Click(g, circle)

						if self.combo >= 5:
							self.health += self.combo * 0.2

					if not self.Collide(circle):
						self.Miss()
						self.health -= 10

					self.click_count += 1

			self.win.fill((0, 0, 0, 0))
			circle.Draw(g)

	def Generate_circle(self, texture_count):
		self.circles.append(circle.Circle(self.win, random.randint(self.width/10, self.playfield[0]), random.randint(self.width/10, self.playfield[1]), self.texture_count))

	def Cursor(self):
		self.cursor_pos = pygame.mouse.get_pos()
		
		self.win.blit(self.cursor_texture, (self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2))

	def Collide(self, circle):
		is_hit = False
		if self.cursor_pos[0] > (circle.x - circle.radius) and self.cursor_pos[1] > (circle.y - circle.radius):
			if self.cursor_pos[0] < (circle.x + circle.radius) and self.cursor_pos[1] < (circle.y + circle.radius):
				is_hit = True

		return is_hit

	def Combo(self):
		text = 'points: ' + str(self.points)
		text_points = self.font.render(text, True, self.combo_color)
		text_combo = self.font.render('combo: ' + str(self.combo), True, (255, 255, 255))
		lenght = len(text)

		self.win.blit(text_points, (self.width - lenght * 25, (self.height - 70)))
		self.win.blit(text_combo, (10, (self.height - 70)))

	def Miss(self):
			print('miss')
			self.combo = 0
			miss_pos = pygame.mouse.get_pos()

			img = self.miss_texture
			self.win.blit(img, miss_pos)

	def HealthBar(self):
		font = pygame.font.SysFont("comicsansms", 12)
		bar_text = font.render('HEALTH', True, (255, 255, 255))
		self.win.blit(bar_text, (self.width/10, 0))

		if self.health > 100:
			self.health = 100

		size_bg = ((self.playfield[0] - self.width/10) * self.maxhealth/self.maxhealth, 30)
		pos = (self.width/10, (self.height/10) - 50)
		bar_bg = pygame.draw.rect(self.win, (128, 128, 128), (pos, size_bg))

		if self.health >= 0:
			size = ((self.playfield[0] - self.width/10) * self.health/self.maxhealth, 30)
			bar = pygame.draw.rect(self.win, (0, 255, 0), (pos, size))


if __name__ == '__main__':
	g = Game(width, height)
	Timer = timer.Timer(240)

	g.Run()


#fix miss!!!