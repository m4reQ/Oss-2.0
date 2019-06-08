import pygame
import circle
import random

pygame.init()

width = 1280
height = 720

darken_percent = 0.50

win = pygame.display.set_mode((width, height))

cursor_texture = pygame.image.load('textures/cursor.png')
cursor_texture = pygame.transform.scale(cursor_texture, (16, 16))
miss_texture = pygame.image.load('textures/miss.png')

bg_textures = []
i = 1
while i <= 10:
        string = 'bg' + str(i)
        bg_textures.append(string)
        i += 1

texture_no = bg_textures[random.randint(0, 9)]
bg_texture = pygame.image.load('textures/backgrounds/' + texture_no + '.jpg')
bg_texture = pygame.transform.scale(bg_texture, (width, height))

dark = pygame.Surface(bg_texture.get_size()).convert_alpha()
dark.fill((0, 0, 0, darken_percent*255))

pygame.mouse.set_visible(False)

def Load_map(file):
	f = open('maps/' + file + '.txt')
	for line in f:
		time = int(line[15:21])
		pos_x = int(line[3:6])
		pos_y = int(line[8:11])

		circles = []
		circles.append(circle.Circle(win, pos_x, pos_y, time, 0))

	f.close()
	return circles
	

class Game():
	def __init__(self, width, height):
		self.time = 0
		self.width = width
		self.height = height
		self.win = win
		self.map = 'test'
		self.is_running = True
		self.circles = Load_map(self.map)
		self.click_count = 0
		self.cursor_pos = (0, 0)
		self.playfield = (self.width - (self.width/10), self.height - (self.height/9))
		self.points = 0
		self.combo = 0
		self.combo_color = (255, 255, 255)
		self.texture_count = 0
		self.cursor_texture = cursor_texture
		self.miss_texture = miss_texture
		self.maxhealth = 100
		self.health = self.maxhealth

	def Run(self):
		while self.is_running:
			self.Draw()
			self.HealthBar()
			self.Combo()
			self.Cursor()
			self.Time()

			pygame.display.update()
			self.time = pygame.time.get_ticks()
			print(self.time)
			
		pygame.quit()
		quit()

	def Draw(self):
		for circle in self.circles:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_z or event.key == pygame.K_x:
						if self.Collide(circle):
							circle.Click(g, circle)

							if self.combo >= 5:
								self.health += 2.5

						if not self.Collide(circle):
							self.Miss()
							self.health -= 10
				if event.type == pygame.QUIT:
					self.is_running = False
			if self.health <= 0:
				self.is_running = False

			
			circle.Draw(g)
		self.win.blit(bg_texture, (0, 0))
		self.win.blit(dark, (0, 0))

	# def Generate_circle(self):
	# 	circle = self.circles[-1]
	# 	return circle

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
		font = pygame.font.SysFont("comicsansms", 48)
		text = 'points: ' + str(self.points)
		text_points = font.render(text, True, self.combo_color)
		text_combo = font.render('combo: ' + str(self.combo), True, (255, 255, 255))
		lenght = len(text)

		self.win.blit(text_points, (self.width - lenght * 25, (self.height - 70)))
		self.win.blit(text_combo, (10, (self.height - 70)))

	def Miss(self):
			self.combo = 0
			miss_pos = pygame.mouse.get_pos()

			img = self.miss_texture
			self.win.blit(img, miss_pos)

	def HealthBar(self):
		font = pygame.font.SysFont("comicsansms", 12)
		bar_text = font.render('HEALTH', True, (255, 255, 255))
		self.win.blit(bar_text, (self.width/10, 0))
		self.health -= 0.15

		if self.health > 100:
			self.health = 100

		size_bg = ((self.playfield[0] - self.width/10) * self.maxhealth/self.maxhealth, 30)
		pos = (self.width/10, (self.height/10) - 50)
		bar_bg = pygame.draw.rect(self.win, (128, 128, 128), (pos, size_bg))

		if self.health >= 0:
			size = ((self.playfield[0] - self.width/10) * self.health/self.maxhealth, 30)
			bar = pygame.draw.rect(self.win, (0, 255, 0), (pos, size))

	def Time(self):
		font = pygame.font.SysFont("comicsansms", 24)
		time = round((self.time/1000), 2)
		text = font.render('Time: ' + str(time) + 's', True, (255, 255, 255))
		pos = (self.width/10, (self.height/10) - 50)

		self.win.blit(text, pos)

if __name__ == '__main__':
	g = Game(width, height)
	Load_map(g.map)
	clock = pygame.time.Clock()
	clock.tick(1000)

	g.Run()

#fix miss!!!
#for miss animation use image.alpha operations
#change indents to NORMAL lenght!!!
