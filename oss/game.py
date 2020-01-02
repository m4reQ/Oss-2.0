try:
	from helper import *
	import pygame
	from launcher import sets
	from launcher import AR, CS, HP
	from launcher import backgroundTextures, interfaceTextures
	from launcher import background_surf
	from launcher import targetFPS
	from launcher import resolution
	from launcher import LauncherInfo
	from eventhandler import keyBindTable
	from utils import *
	import time
	import random
	from eventhandler import EventHandler
	import GameElements.circle as circle
	import GameElements.map as map
	import GameElements.interface as interface
except ImportError as e:
	print(e)
	logError(e)
	
	pygame.quit()
	quit()
#import cuncurrent.futures ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

#import cuncurrent.futures ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

#create settings shortcuts
DEBUG_MODE = sets.DEBUG_MODE
TEST_MODE = sets.TEST_MODE
DICT_UPDATE_MODE = sets.DICT_UPDATE_MODE

#create textures shortcuts
cursor_texture = interfaceTextures.GetTexture('cursor')
miss_texture = interfaceTextures.GetTexture('miss')
bg_texture = backgroundTextures.GetTexture('bg_{}'.format(random.randint(0, backgroundTextures.count - 2)))

#called once to update window background
@run_once
def pre_update_display():
	if DEBUG_MODE:
		print('[INFO]<{}> Updating screen.'.format(__name__))
	pygame.display.update()

#timed updates
@run_interval(interval=10)
def timed_update_display():
	if DEBUG_MODE:
		print('[INFO]<{}> Updating screen.'.format(__name__))
	pygame.display.update()

class Game():
	def __init__(self, win, parentWin):
		self.clock = pygame.time.Clock()
		self.time = 0
		self.win = win
		self.menu = parentWin
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

		interface.changeFont('comicsansms', 48)

		self.cursor = interface.InterfaceElement(cursor_texture.get_width(), cursor_texture.get_height(), self.cursor_pos, image=cursor_texture)
		self.combo_text = interface.InterfaceElement(0, 55, position=(10, self.height - 70), textColor=color.white)
		self.points_text = interface.InterfaceElement(0, 55, position=(0, self.height - 70), textColor=color.random())

		#at the end of initialization trigger garbage collection
		FreeMem(DEBUG_MODE, 'Started after-init garbage collection.')

	def Render(self):
		self.DrawPlayGround()
		if self.draw_interface:
			self.DrawCombo()
			self.DrawHealthBar()
			self.DrawPoints()
			self.DrawTime()
			self.DrawClicksCounter()
			if DEBUG_MODE:
				self.DrawFPSCounter()
		self.DrawCursor()

	def RenderConcurrently(self):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.submit(self.DrawPlayGround)
			if self.draw_interface:
				executor.submit(self.DrawHealthBar)
				executor.submit(self.DrawCombo)
				executor.submit(self.DrawPoints)
				executor.submit(self.DrawTime)
				executor.submit(self.DrawClicksCounter)
				if DEBUG_MODE:
					executor.submit(self.DrawFPSCounter)
			executor.submit(self.DrawCursor)

	def Run(self):
		global DEBUG_MODE
		
		if not sets.auto_generate:
			map_data = map.Load_map('test')
			self.circles = map.Make_map(map_data, (self.width, self.height))

			if type(self.circles).__name__ == 'str' or type(self.circles).__name__ == 'NoneType':
				raise Exception('[ERROR] An error appeared during map loading.')
		
		#free memory after map loading
		FreeMem(DEBUG_MODE, 'Started after map loading garbage collection.')
		
		maxRadius = stats.getCS(1)

		while self.is_running:
			self.events = pygame.event.get()

			if sets.auto_generate:
				if len(self.circles) < 1:
					obj = circle.Circle(random.randint(int(self.playfield['topX'] + maxRadius), int(self.playfield['bottomX'] - maxRadius)), random.randint(int(self.playfield['topX'] + maxRadius), int(self.playfield['bottomY'] - maxRadius)))
					self.circles.append(obj)

			#event handling
			for event in self.events: 
				self.cursor_pos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					EventHandler.HandleKeys(self, event)

				EventHandler.HandleEvents(self, event)

			EventHandler.HandleInternalEvents(self)

			self.health -= stats.getHP(self.HP) * self.render_time * 79.2 #constant to compensate FPS multiplication

			if DEBUG_MODE and len(self.circles) < 5:
				print('[INFO]<{}> Circle list: {}.'.format(__name__, str(self.circles)))
			if DEBUG_MODE and len(self.circles) >= 5:
				print('[INFO]<{}> Circle list Minimized. Contains: {} circles.'.format(__name__, len(self.circles)))

			#render
			#drawing section
			#NOTE!
			#Don't put anything below this section
			#it may cause glitches
			if LauncherInfo.concurrencyAvailable: self.RenderConcurrently()
			else: self.Render()

			#update
			if DICT_UPDATE_MODE: #dictionary update
				pre_update_display()
				pygame.display.update(self.toUpdate)
				if DEBUG_MODE:
					print('[INFO]<{}> Updating: {}.'.format(__name__, str(self.toUpdate)))

				self.toUpdate.clear()

				if sets.timed_updates_enable:
					timed_update_display()
			if not DICT_UPDATE_MODE: #standard update (window update)
				pygame.display.flip()

			#calculate fps etc.
			if targetFPS == 0:
				self.clock.tick()
			else:
				self.clock.tick(targetFPS)

			self.fps = int(self.clock.get_fps())
			self.render_time = round(self.clock.get_time(), 3) / 1000
			self.time = pygame.time.get_ticks() - self.menu.time
		
		#close if game has ended
		self.Close()
	
	def Close(self):
		self.menu.game = None
		map.is_loaded = False

		circle.Circle.count = 0
		circle.Circle.texture_count = 0
		circle.Circle.background_count = 0

		del(self)
		FreeMem(DEBUG_MODE, 'Started onclose garbage collection.')

	def DrawPlayGround(self):
		self.win.blit(bg_texture, (0, 0))

		for circle in self.circles:
			#get top circle (the first circle added)
			topCircle = self.circles[0]
			if not sets.auto_generate: #in case of playing a map
				if self.time >= circle.startTime and self.time <= circle.startTime + stats.getAR(self.AR):
					circle.Draw(self.win)  
					for event in self.events:
						if event.type == pygame.KEYDOWN:
							if event.key == keyBindTable['kl'] or event.key == keyBindTable['kr']:
								if topCircle.Collide(self.cursor_pos):
									topCircle.Hit(self)
								else:
									topCircle.Miss(self)
						if event.type == pygame.MOUSEBUTTONDOWN:
							if event.button == 1:
								self.click_count[0] += 1
							elif event.button == 3:
								self.click_count[1] += 1

							if topCircle.Collide(self.cursor_pos):
								topCircle.Hit(self)
							else:
								topCircle.Miss(self)

				elif self.time >= topCircle.startTime + stats.getAR(self.AR):
					topCircle.Miss(self)
			else: #in case of playing in auto generate mode
				circle.Draw(self.win)  
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if event.key == keyBindTable['kl'] or event.key == keyBindTable['kr']:
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
		time = round((self.time/float(1000)), 2)
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