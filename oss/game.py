if __name__ == '__main__':
	quit()

try:
	from helper import *
	import pygame
	from launcher import sets
	from launcher import AR, HP, CS
	from launcher import mainResManager
	from launcher import resolution
	from launcher import LauncherInfo
	from eventhandler import keyBindTable
	import time
	from utils import *
	import time
	import random
	from eventhandler import EventHandler
	from GameElements.circle import Circle
	from GameElements.map import Map, EmptyMap
except ImportError as e:
	print(e)
	logError(e)
	
	pygame.quit()
	quit()
#import cuncurrent.futures ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

#create settings shortcuts
DEBUG_MODE = sets.DEBUG_MODE
TEST_MODE = sets.TEST_MODE
DICT_UPDATE_MODE = sets.DICT_UPDATE_MODE

#called once to update window background
@run_once
def pre_update_display():
	if DEBUG_MODE:
		print('[INFO]<{}> Updating screen.'.format(__name__))
	pygame.display.update()

class Game():
	def __init__(self, win, parentWin):
		self.win = win
		self.menu = parentWin
		self.width = win.get_width()
		self.height = win.get_height()
		self.isRunning = True
		self.click_count = [0, 0] #[0] stands for left key, [1] for right
		self.cursorPos = (0, 0)
		self.map = None
		self.circles = []
		self.playfield = {
		'topLeft': (self.width / 10 + CS, self.height / 10 + CS),
		'topRight': (self.width - self.width / 10 - CS, self.height / 10 + CS),
		'bottomLeft': (self.width / 10 + CS, self.height - self.height / 10 - CS),
		'bottomRight': (self.width - self.width / 10 - CS, self.height - self.height / 10 - CS),
		'minX': int(self.width / 10 + CS),
		'minY': int(self.height / 10 + CS),
		'maxX': int(self.width - self.width / 10 - CS),
		'maxY': int(self.height - self.height / 10 - CS)}
		self.points = 0
		self.combo = 0
		self.maxhealth = 100
		self.pointsColor = color.random()
		self.health = self.maxhealth
		self.frameTime = 0.0
		self.fps = 0.0
		self.time = 0.0
		self.time_ms = 0
		self.draw_interface = True
		self.toUpdate = []
		self.backgroundName = 'bg_' + str(random.randint(0, 6))
		self.events = pygame.event.get()

		#at the end of initialization trigger garbage collection
		FreeMem(DEBUG_MODE, 'Started after-init garbage collection.')

	def Render(self):
		self.DrawPlayGround()
		if self.draw_interface:
			self.DrawCombo()
			self.DrawHealthBar()
			self.DrawPoints()
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
				executor.submit(self.DrawClicksCounter)
				if DEBUG_MODE:
					executor.submit(self.DrawFPSCounter)
			executor.submit(self.DrawCursor)

	def Run(self):
		global DEBUG_MODE
		
		if not sets.auto_generate:
			Map.resolution = (self.width, self.height)
			self.map = Map('Resources/maps/test.txt')
		else:
			self.map = EmptyMap()
			self.GenerateRandomCircle()

		if self.map.loadSuccess == -1:
			if DEBUG_MODE:
				print('[ERROR]<{}> An error appeared during map loading.'.format(__name__))
			self.isRunning = False
		
		#free memory after map loading
		FreeMem(DEBUG_MODE, 'Started after map loading garbage collection.')

		while self.isRunning:
			if LauncherInfo.timePerfCounterAvailable:
				start = time.perf_counter()
			else:
				start = time.time()
			
			self.events = pygame.event.get()

			#event handling
			for event in self.events: 
				self.cursorPos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					EventHandler.HandleKeys(self, event)

				EventHandler.HandleEvents(self, event)

			EventHandler.HandleInternalEvents(self)

			self.health -= HP * self.frameTime * 79.2 #constant to compensate FPS multiplication

			#render
			#drawing section
			#NOTE!
			#Don't put anything below this section
			#it may cause glitches
			#update
			if DICT_UPDATE_MODE: #dictionary update
				pre_update_display()
				pygame.display.update(self.toUpdate)
				if DEBUG_MODE:
					print('[INFO]<{}> Updating: {}.'.format(__name__, str(self.toUpdate)))

				self.toUpdate.clear()
					
			pygame.display.flip()

			#render
			self.RenderConcurrently() if LauncherInfo.concurrencyAvailable else self.Render()

			#calculate fps etc.
			if sets.use_fps_cap:
				time.sleep(1.0 / 120.0)

			if LauncherInfo.timePerfCounterAvailable:
				self.frameTime = time.perf_counter() - start
			else:
				self.frameTime = time.time() - start

			self.fps = float(1.0 / self.frameTime)
			self.time += self.frameTime
			self.time_ms += self.frameTime * 1000
		
		#close if game has ended
		self.Close()
	
	def GenerateRandomCircle(self):
		pos = (random.randint(self.playfield['minX'], self.playfield['maxX']), random.randint(self.playfield['minY'], self.playfield['maxY']))
		obj = Circle(pos, -1)
		self.map.objectsLeft.append(obj)
	
	def Close(self):
		self.menu.game = None

		Circle.count = 0
		Circle.texture_count = 0
		Circle.background_count = 0

		FreeMem(DEBUG_MODE, 'Started onclose garbage collection.')

	def DrawPlayGround(self):
		self.win.blit(mainResManager.GetTexture(self.backgroundName).Get(), (0, 0))

		if len(self.map.objectsLeft) == 0:
			return

		#get the top circle (first circle active)
		for circle in self.map.objectsLeft:
			if not circle.destroyed:
				topCircle = circle
				break

		for circle in self.map.objectsLeft:
			circle.Update(self)
			if not sets.auto_generate: #in case of playing a map
				if self.time_ms >= circle.startTime and self.time_ms <= circle.endTime:
					circle.Draw(self.win)  
					if self.time_ms >= circle.hitTime and self.time_ms <= circle.endTime:
						circle.DrawLayout(self.win)
						
					for event in self.events:
						if event.type == pygame.KEYDOWN:
							if event.key == keyBindTable['kl'] or event.key == keyBindTable['kr']:
								topCircle.Collide(self, self.cursorPos)

						if event.type == pygame.MOUSEBUTTONDOWN:
							EventHandler.HandleMouse(self, event)
							topCircle.Collide(self, self.cursorPos)

				elif self.time_ms > topCircle.endTime:
					topCircle.Miss(self)
			else: #in case of playing in auto generate mode
				circle.Draw(self.win)  
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if event.key == keyBindTable['kl'] or event.key == keyBindTable['kr']:
							topCircle.Collide(self, self.cursorPos)

					if event.type == pygame.MOUSEBUTTONDOWN:
						EventHandler.HandleMouse(self, event)
						topCircle.Collide(self, self.cursorPos)
							
	def DrawCursor(self):
		self.win.blit(mainResManager.GetTexture('cursor').Get(), (self.cursorPos[0] - mainResManager.GetTexture('cursor').Width / 2, self.cursorPos[1] - mainResManager.GetTexture('cursor').Height / 2))

	def DrawCombo(self):
		font = mainResManager.GetFont("comicsansms_48")

		rText = font.render('combo: {}'.format(self.combo), True, color.white)

		pos = (3, self.height - rText.get_height() - 3 - 12)
		self.win.blit(rText, pos)

	def DrawPoints(self):
		font = mainResManager.GetFont("comicsansms_48")

		rText = font.render('points: {}'.format(self.points), True, self.pointsColor)

		pos = (self.width - rText.get_width() - 3, self.height - rText.get_height() - 3 - 12)

		self.win.blit(rText, pos)

	def DrawHealthBar(self):
		bgSize = (self.width - (2 * self.width / 10), self.height / 10)
		barSize = ((self.width - (2 * self.width / 10)) * (self.health / self.maxhealth), self.height / 10)
		pos = (self.width / 10, 0)

		barBgRect = pygame.Rect(pos, bgSize)

		if self.health <= self.maxhealth / 5:
			c = color.red
		else:
			c = color.green

		pygame.draw.rect(self.win, color.gray, (pos, bgSize))
		pygame.draw.rect(self.win, c, (pos, barSize))

		font = mainResManager.GetFont("comicsansms_24")
		rText = font.render('Time: {}s'.format(round(self.time, 2)), True, color.white)

		self.win.blit(rText, (barBgRect.x, barBgRect.centery - rText.get_height() / 2))

	def DrawClicksCounter(self):
		font = mainResManager.GetFont("comicsansms_24")
		rTextLeft = font.render(str(self.click_count[0]), True, color.white)
		rTextRight = font.render(str(self.click_count[1]), True, color.white)

		leftPos = (self.width - rTextLeft.get_width() - 3, self.height / 2 - rTextLeft.get_height() / 2)
		rightPos = (self.width - rTextRight.get_width() - 3, self.height / 2 + rTextRight.get_height() / 2)

		self.win.blit(rTextLeft, leftPos)
		self.win.blit(rTextRight, rightPos)

	def DrawFPSCounter(self):
		font = mainResManager.GetFont("comicsansms_12")
		text = 'Frame time: {}ms | FPS: {}'.format(round(self.frameTime * 1000, 3), round(self.fps, 3))
		rText = font.render(text, True, color.white)
		pos = (int(self.width - 38 * 6), self.height - rText.get_height() - 2)

		self.win.blit(rText, pos)