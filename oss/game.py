if __name__ == '__main__':
	import sys
	sys.exit()

try:
	import pygame
	from launcher import debugging, AR, HP, CS, mainResManager, prefs
	from eventhandler import EventHandler
	from Utils.performance import FreeMem, Profiler, RenderStats
	from Utils.graphics import Color
	from Utils.game import Stats, GetPlayfield
	from GUIElements.GameGUI.fpsCounter import *
	from GUIElements.GameGUI.healthBar import *
	from GUIElements.GameGUI.pointsCounter import *
	from GUIElements.GameGUI.comboCounter import *
	from GUIElements.GameGUI.clicksCounter import *
	try:
		from time import perf_counter as timer
	except (ImportError, ModuleNotFoundError):
		from time import time as timer
	import time
	import random
	from eventhandler import EventHandler
	from GameElements.circle import Circle
	from GameElements.map import Map, EmptyMap
except ImportError:
	print("Cannot load game.")
	raise

class Game:
	@classmethod
	def Start(cls, win, menu):
		inst = cls(win, menu)
		menu.game = inst
		inst.Run()

	def __init__(self, win, menu):
		self.win = win
		self.menu = menu
		self.width = win.get_width()
		self.height = win.get_height()
		self.isRunning = True
		self.click_count = [0, 0] #[0] stands for left key, [1] for right
		self.cursorPos = (0, 0)
		self.map = None
		self.circles = []
		self.playfield = GetPlayfield(self.width, self.height, CS)
		self.points = 0
		self.combo = 0
		self.maxHealth = 100
		self.health = self.maxHealth

		self.eventHandler = EventHandler(self)
		
		self.draw_interface = True
		self.toUpdate = []
		self.backgroundName = 'bg_' + str(random.randint(0, 6))
		self.events = pygame.event.get()

		self.renderStats = RenderStats()

		self.clock = pygame.time.Clock()

		#GUI elements
		if prefs.useNewFpsCounter:
			self.fpsCounter = NewStyleFpsCounter(mainResManager.GetFont("comicsansms_10"), (self.width - 2, 27), (113, 110))
			print('[WARNING]<{}> Using new style fps counter. This may decrease performance.'.format(__name__))
		else:
			self.fpsCounter = FpsCounter(mainResManager.GetFont("comicsansms_12"), (self.width - 2, self.height - 2))
		self.healthBar = HealthBar(mainResManager.GetFont("comicsansms_22"), (self.width / 10, 0), (self.width - (2 * self.width / 10), 25))
		self.pointsText = PointsCounter(mainResManager.GetFont("comicsansms_48"), (self.width - 2, self.height - 14))
		self.comboText = ComboCounter(mainResManager.GetFont("comicsansms_48"), (2, self.height - 14))
		self.clicksText = ClicksCounter(mainResManager.GetFont("comicsansms_21"), (self.width - 2, self.height / 2))

		self.time = 0.0
		self.time_ms = 0
		
		self.profiler = None
		if debugging:
			self.profiling = False
			self.profiler = Profiler()

		#at the end of initialization trigger garbage collection
		FreeMem(debugging, 'Started after-init garbage collection.')

	def Run(self):
		if not prefs.autoGenerate:
			Map.resolution = (self.width, self.height)
			self.map = Map('Resources/maps/test.txt')
		else:
			self.map = EmptyMap()
			self.GenerateRandomCircle()

		if self.map.loadSuccess == -1:
			if debugging:
				print('[ERROR]<{}> An error appeared during map loading.'.format(__name__))
			self.menu.AddMessage("An error appeared during map loading.")
			self.isRunning = False

		#free memory after map loading
		FreeMem(debugging, 'Started after map loading garbage collection.')

		while self.isRunning:
			self.renderStats.Reset()

			frameTimeStart = timer()
			
			eventTimeStart = timer()
			self.events = pygame.event.get()

			#event handling
			for event in self.events: 
				if event.type == pygame.MOUSEMOTION:
					self.cursorPos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					self.eventHandler.HandleKeys(event)
				
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.eventHandler.HandleMouse(event)

				self.eventHandler.HandleEvents(event)

			self.eventHandler.HandleInternalEvents()

			self.health -= HP * self.renderStats.frameTime * 79.2

			#get total blits count
			self.renderStats.blitCount += self.pointsText.blitsRequired + self.comboText.blitsRequired + self.fpsCounter.blitsRequired + self.healthBar.blitsRequired + self.clicksText.blitsRequired
			if self.profiling:
				self.renderStats.blitCount += 1

			self.renderStats.eventHandlingTime = timer() - eventTimeStart

			#render
			#drawing section
			#NOTE!
			#Don't put anything below this section
			#it may cause glitches
			renderTimeStart = timer()
			playgroundTimeStart = timer()
			self.DrawPlayGround()
			self.renderStats.playgroundDrawTime = timer() - playgroundTimeStart
			if self.draw_interface:
				self.DrawGui()
			self.DrawCursor()

			self.renderStats.renderTime = timer() - renderTimeStart

			updateTimeStart = timer()

			pygame.display.flip()

			self.renderStats.updateTime = timer() - updateTimeStart

			#calculate fps etc.
			if prefs.useFpsCap:
				waitTimeStart = timer()
				self.clock.tick(prefs.targetFps)
				self.renderStats.waitTime = timer() - waitTimeStart

			self.renderStats.frameTime = timer() - frameTimeStart

			self.time += self.renderStats.frameTime
			self.time_ms += self.renderStats.frameTime * 1000

			#debug only code idk if this should be in release
			if self.profiler and self.profiling:
				self.profiler.Profile(self.renderStats.frameTime)
		
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

		FreeMem(debugging, 'Started onclose garbage collection.')

		if getattr(self.profiler, "used", False):
			print(self.profiler.GetProfileData())
			self.profiler.SaveProfileData("perfLog.txt")

	def DrawPlayGround(self):
		self.win.blit(mainResManager.GetTexture(self.backgroundName).Get(), (0, 0))
		self.renderStats.blitCount += 1

		if len(self.map.objectsLeft) == 0:
			return

		#get the top circle (first circle active)
		for circle in self.map.objectsLeft:
			if not circle.destroyed:
				topCircle = circle
				break

		for circle in self.map.objectsLeft:
			circle.Update(self)
			if self.time_ms >= circle.startTime and self.time_ms <= circle.endTime:
				circle.Draw(self.win, self.time_ms, self)
						
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if event.key == prefs.keyBinds['kl'] or event.key == prefs.keyBinds['kr']:
							topCircle.Collide(self, self.cursorPos)
					
					if event.type == pygame.MOUSEBUTTONDOWN and not prefs.mouseButtonsDisable:
						EventHandler.HandleMouse(self, event)
						topCircle.Collide(self, self.cursorPos)
			elif self.time_ms > circle.endTime:
				topCircle.Miss(self)
							
	def DrawCursor(self):
		tex = mainResManager.GetTexture('cursor')
		self.win.blit(tex.Get(), (self.cursorPos[0] - tex.Width / 2, self.cursorPos[1] - tex.Height / 2))
		self.renderStats.blitCount += 1
	
	def DrawGui(self):
		self.comboText.Render(self.win, self.combo)
		self.healthBar.Render(self.win, self.health, self.maxHealth, self.time)
		self.pointsText.Render(self.win, self.points)
		self.clicksText.Render(self.win, self.click_count[0], self.click_count[1])
		if debugging:
			if prefs.useNewFpsCounter:
				self.fpsCounter.Render(self.win, self.profiling, self.renderStats.frameTime, self.renderStats.renderTime, self.renderStats.updateTime, self.renderStats.eventHandlingTime, self.renderStats.playgroundDrawTime, self.renderStats.waitTime, self.renderStats.blitCount)
			else:
				self.fpsCounter.Render(self.win, self.profiling, self.renderStats.frameTime)

		

	