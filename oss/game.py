try:
	import os
except ImportError:
	print('Critical error! Cannot load os module.')
	exit()

try:
	from helper import *
	import pygame
	from launcher import sets
	from launcher import AR, CS, HP
	from launcher import backgroundTextures, interfaceTextures
	from launcher import background_surf
	from launcher import targetFPS
	from launcher import resolution
	from eventhandler import keyBindTable
	from utils import *
	import time
	import random
	import concurrent.futures
	from eventhandler import EventHandler
	import GameElements.circle as circle
	import GameElements.map as map
	import GameElements.interface as interface
except ImportError as e:
	print(e)
	logError(e)
	
	exitAll()

#####developer settings#####
#NOTE!
#All developer settings are variables 
#in capital letters
DEBUG_MODE = sets.DEBUG_MODE
TEST_MODE = sets.TEST_MODE

#dictionary update mode
DICT_UPDATE_MODE = sets.DICT_UPDATE_MODE

#####STATICS#####
#key binding
left_key = keyBindTable['kl']
right_key = keyBindTable['kr']

#textures loading
cursor_texture = interfaceTextures.GetTexture('cursor')
miss_texture = interfaceTextures.GetTexture('miss')
bg_texture = backgroundTextures.GetTexture('bg_' + str(random.randint(0, backgroundTextures.count - 2)))

#surfaces initialization
bg_surf = background_surf

#called once to update window background
@run_once
def pre_update_display():
	if DEBUG_MODE:
		print('[INFO]<', str(__name__), '> Updating screen.')
	pygame.display.update()

@run_interval(interval=10)
def timed_update_display():
	if DEBUG_MODE:
		print('[INFO]<', str(__name__), '> Updating screen.')
	pygame.display.update()

class Game():
	def __init__(self, win, parentWin):
		self.clock = pygame.time.Clock()
		self.time = 0
		self.win = win
		self.width = win.get_width()
		self.height = win.get_height()
		self.is_running = True
		self.click_count = [0, 0] #[0] stands for left key, [1] for right
		self.cursor_pos = (0, 0)
		self.circles = []
		self.playfield = {
		'topX': (self.width / 10 + int(stats.getCS(1) / 2)),
		'topY': (self.height / 10 + int(stats.getCS(1) / 2)),
		'bottomX': (self.width - self.width / 10 - int(stats.getCS(1) / 2)),
		'bottomY': (self.height - self.height / 10 - int(stats.getCS(1) / 2))}
		self.points = 0
		self.combo = 0
		self.maxhealth = 100
		self.health = self.maxhealth
		self.AR = AR
		self.CS = CS
		self.HP = HP
		self.render_time = 0
		self.fps = 0
		self.events = pygame.event.get()
		self.draw_interface = True
		self.toUpdate = []
		self.menu = parentWin

		interface.changeFont('comicsansms', 48)

		self.cursor = interface.InterfaceElement(cursor_texture.get_width(), cursor_texture.get_height(), self.cursor_pos, image=cursor_texture)
		self.combo_text = interface.InterfaceElement(0, 55, position=(10, self.height - 70), textColor=color.white)
		self.points_text = interface.InterfaceElement(0, 55, position=(0, self.height - 70), textColor=color.random())

	def Run(self):
		global DEBUG_MODE
		
		if not sets.auto_generate:
			map_data = map.Load_map('test')
			self.circles = map.Make_map(map_data, (self.width, self.height))

			if type(self.circles).__name__ == 'str' or type(self.circles).__name__ == 'NoneType':
				raise Exception('[ERROR] An error appeared during map loading.')
		
		radius = stats.getCS(1)

		while self.is_running:
			self.events = pygame.event.get()

			if sets.auto_generate:
				if len(self.circles) < 1:
					obj = circle.Circle(random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomX'] - radius)), random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomY'] - radius)))
					self.circles.append(obj)

			#event handling
			for event in self.events: 
				self.cursor_pos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					EventHandler.HandleKeys(self, event)

				EventHandler.HandleEvents(self, event)

			EventHandler.HandleInternalEvents(self)

			self.health -= stats.getHP(self.HP) * self.render_time   * 79.2 #constant to compensate FPS multiplication

			if DEBUG_MODE and len(self.circles) < 5:
				print('[INFO]<', str(__name__), '> ', str(self.circles))
			if DEBUG_MODE and len(self.circles) >= 5:
				print('[INFO]<', str(__name__), '> Circle list Minimized. Contains: ', str(len(self.circles)), ' circles')

			#render
			#drawing section
			#NOTE!
			#Don't put anything below this section
			#it may cause glitches
			with concurrent.futures.ThreadPoolExecutor() as executor:
				executor.submit(self.DrawPlayGround)
				if self.draw_interface:
					executor.submit(self.DrawHealthBar)
					executor.submit(self.DrawCursor)
					executor.submit(self.DrawCombo)
					executor.submit(self.DrawPoints)
					executor.submit(self.DrawTime)
					executor.submit(self.DrawClicksCounter)
					if DEBUG_MODE:
						executor.submit(self.DrawFPSCounter)
				executor.submit(self.DrawCursor)

			#update
			#####implement rects dictionary update here #####
			pre_update_display()

			if DICT_UPDATE_MODE:
				pygame.display.update(self.toUpdate)
				print('[INFO]<', str(__name__), '> Updating: ', str(self.toUpdate))

				self.toUpdate.clear()

				if sets.timed_updates_enable:
					timed_update_display()
			#####end of implementation##### 
			if not DICT_UPDATE_MODE:
				pygame.display.flip()

			if targetFPS == 0:
				self.clock.tick()
			else:
				self.clock.tick(targetFPS)

			self.fps = int(self.clock.get_fps())
			self.render_time = round(self.clock.get_time(), 3) / 1000
			self.time = pygame.time.get_ticks() - self.menu.time
		
		self.Close()
	
	def Close(self):
		self.menu.game = None

	def DrawPlayGround(self):
		self.win.blit(bg_texture, (0, 0))

		for circle in self.circles:
			if not sets.auto_generate: #in case of playing a map
				if self.time >= circle.time and self.time <= circle.time + stats.getAR(self.AR):
					circle.Draw(self.win)  
					for event in self.events:
						if event.type == pygame.KEYDOWN:
							if event.key == pygame.K_z or event.key == pygame.K_x:
								if circle.Collide(self.cursor_pos):
									circle.Hit(self)
								else:
									circle.Miss(self)
						if event.type == pygame.MOUSEBUTTONDOWN:
							if event.button == 1:
								self.click_count[0] += 1
							elif event.button == 3:
								self.click_count[1] += 1

							if circle.Collide(self.cursor_pos):
								circle.Hit(self)
							else:
								circle.Miss(self)

				elif self.time >= circle.time + stats.getAR(self.AR):
					circle.Miss(self)
			else: #in case of playing in auto generate mode
				circle.Draw(self.win)  
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if event.key == pygame.K_z or event.key == pygame.K_x:
							if circle.Collide(self.cursor_pos):
								circle.Hit(self)
							else:
								circle.Miss(self)
					if event.type == pygame.MOUSEBUTTONDOWN:
						if event.button == 1:
							self.click_count[0] += 1
						elif event.button == 3:
							self.click_count[1] += 1

						if circle.Collide(self.cursor_pos):
							circle.Hit(self)
						else:
							circle.Miss(self)
							
	def DrawCursor(self):
		self.cursor.positionX = self.cursor_pos[0] - self.cursor.width/2
		self.cursor.positionY = self.cursor_pos[1] - self.cursor.height/2

		self.cursor.Render(self.win)

		rect = self.cursor.getRect()

		if not rect in self.toUpdate:
			self.toUpdate.append(rect)

	def DrawCombo(self):
		interface.changeFont('comicsansms', 48)

		text = 'combo: ' + str(self.combo)

		self.combo_text.text = text
		self.combo_text.width = len(text) * 25

		self.combo_text.Render(self.win)

		rect = self.combo_text.getRect()

		if not rect in self.toUpdate:
			self.toUpdate.append(rect)

	def DrawPoints(self):
		text = 'points: ' + str(self.points)
		
		self.points_text.text = text
		self.points_text.width = len(text) * 24 - 5
		self.points_text.textPositionX = (self.width - len(text) * 24)

		self.points_text.Render(self.win)

		rect = self.points_text.getRect()

		if not rect in self.toUpdate:
			self.toUpdate.append(rect)

	def DrawHealthBar(self):
		size_bg = (self.width - (2 * self.width/10), 30)
		pos = (self.width/10, 0)
		pygame.draw.rect(self.win, color.gray, (pos, size_bg))

		if self.health <= self.maxhealth/5:
			c = color.red
		else:
			c = color.green

		size = ((self.playfield['bottomX'] - self.width/10) * self.health/self.maxhealth, 30)
		pygame.draw.rect(self.win, c, (pos, size))

		rect = pygame.Rect((pos[0], pos[1]), (self.width - (2 * self.width/10), 30))

		if not rect in self.toUpdate:
			self.toUpdate.append(rect)

	def DrawTime(self):
		font = pygame.font.SysFont("comicsansms", 24)
		time = round((self.time/1000), 2)
		text = font.render('Time: ' + str(time) + 's', True, color.white)
		pos = (self.width/10, 0)

		self.win.blit(text, pos)

	def DrawClicksCounter(self):
		font = pygame.font.SysFont("comicsansms", 24)
		text_left = font.render(str(self.click_count[0]), True, color.white)
		text_right = font.render(str(self.click_count[1]), True, color.white)
		pos_left = ((self.width - (18*len(str(self.click_count[0])))), (self.height/2))
		pos_right = ((self.width - (18*len(str(self.click_count[1])))), (self.height/2 + 28))

		self.win.blit(text_left, pos_left)
		self.win.blit(text_right, pos_right)

	def DrawFPSCounter(self):
		font = pygame.font.SysFont("comicsansms", 12)
		text = 'Render time: ' + str(self.render_time*1000) + 'ms | FPS: ' + str(self.fps)
		r_text = font.render(text, True, color.white)
		pos = (self.width - len(text) * 7, self.height - 80)

		max_length = (len(text)+3)

		self.win.blit(r_text, pos)

		rect = pygame.Rect((pos[0], pos[1]), (max_length * 7, 18))

		if not rect in self.toUpdate:
			self.toUpdate.append(rect)

if __name__ == '__main__':
	pygame.quit()
	quit()