if __name__ == '__main__':
	import sys
	sys.exit()

try:
	import pygame
	import threading
	import time
	import random
	try:
		from time import perf_counter as timer
	except (ImportError, ModuleNotFoundError):
		from time import time as timer

	from launcher import AR, HP, CS, mainResManager, prefs
	from Utils.performance import FreeMem, RenderStats
	from Utils.graphics import Color
	from Utils.game import Stats, GetPlayfield
	from Utils import debug
	from GUIElements.GameGUI.fpsCounter import *
	from GUIElements.GameGUI.healthBar import *
	from GUIElements.GameGUI.pointsCounter import *
	from GUIElements.GameGUI.comboCounter import *
	from GUIElements.GameGUI.clicksCounter import *
	from Utils.debug import Log, LogLevel
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
		self.clickCount = [0, 0] #[0] stands for left key, [1] for right
		self.cursorPos = (0, 0)
		self.map = None
		self.playfield = GetPlayfield(self.width, self.height, CS)
		self.points = 0
		self.combo = 0
		self.maxHealth = 100
		self.health = self.maxHealth

		self.buttonClicked = False
		
		self.drawInterface = True
		self.backgroundName = 'bg_' + str(random.randint(0, 6))
		self.events = pygame.event.get()

		self.renderStats = RenderStats()

		self.clock = pygame.time.Clock()

		#GUI elements
		if prefs.useNewFpsCounter:
			self.fpsCounter = NewStyleFpsCounter(mainResManager.GetFont("comicsansms_10"), (self.width - 2, 27), (113, 110))
			Log("Using new style fps counter. This may decrease performance.", LogLevel.Warning, __name__)
		else:
			self.fpsCounter = FpsCounter(mainResManager.GetFont("comicsansms_12"), (self.width - 2, self.height - 2))

		self.healthBar = HealthBar(mainResManager.GetFont("comicsansms_22"), (self.width / 10, 0), (self.width - (2 * self.width / 10), 25))
		self.pointsText = PointsCounter(mainResManager.GetFont("comicsansms_48"), (self.width - 2, self.height - 14))
		self.comboText = ComboCounter(mainResManager.GetFont("comicsansms_48"), (2, self.height - 14))
		self.clicksText = ClicksCounter(mainResManager.GetFont("comicsansms_21"), (self.width - 2, self.height / 2))

		self.time = 0.0
		self.time_ms = 0

		self.renderThread = threading.Thread(target=self.Render, name="ossRender")

		#at the end of initialization trigger garbage collection
		FreeMem('Started after-init garbage collection.')

	def __UpdateCircles(self):
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
				circle.shouldDraw = True
						
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if self.buttonClicked:
							topCircle.Collide(self, self.cursorPos)
					
					if event.type == pygame.MOUSEBUTTONDOWN and not prefs.mouseButtonsDisable:
						topCircle.Collide(self, self.cursorPos)

			elif self.time_ms > circle.endTime:
				topCircle.Miss(self)

	def Render(self):
		while self.isRunning:
			renderStart = timer()

			playgroundStart = timer()
			self.win.blit(mainResManager.GetTexture(self.backgroundName).Get(), (0, 0))
			self.renderStats.blitCount += 1

			for circle in self.map.objectsLeft:
				circle.Draw(self.win, self.time_ms, self)
			
			self.renderStats.playgroundDrawTime = timer() - playgroundStart
			
			if self.drawInterface:
				self.DrawGui()

			self.DrawCursor()

			pygame.display.flip()

			if prefs.useFpsCap:
				waitStart = timer()
				self.clock.tick(prefs.targetFps)
				self.renderStats.waitTime = timer() - waitStart

			self.renderStats.renderTime = timer() - renderStart
			self.time += self.renderStats.renderTime
			self.time_ms += self.renderStats.renderTime * 1000
		
	def Update(self):
		updateStart = timer()

		eventStart = timer()
		self.events = pygame.event.get()
		
		for event in self.events: 
			if event.type == pygame.MOUSEMOTION:
				self.cursorPos = pygame.mouse.get_pos()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.isRunning = False
					Log("User interruption by closing window.", LogLevel.Info, __name__)
						
				if event.key == prefs.keyBinds['hideInterface']:
					self.drawInterface = not self.drawInterface
					Log("Interface hidden.", LogLevel.Info, __name__)
				
				if event.key == prefs.keyBinds['kl']:
					self.clickCount[0] += 1
					self.buttonClicked = True
				if event.key == prefs.keyBinds['kr']:
					self.clickCount[1] += 1
					self.buttonClicked = True
				
				if event.key != prefs.keyBinds['kl'] and event.key != prefs.keyBinds['kr']:
					self.buttonClicked = False
				
			if event.type == pygame.MOUSEBUTTONDOWN and not prefs.mouseButtonsDisable:
				if event.button == 1:
					self.clickCount[0] += 1
				elif event.button == 3:
					self.clickCount[1] += 1

			if event.type == pygame.QUIT:
				self.isRunning = False
				
				Log("User interruption by closing window.", LogLevel.Info, __name__)
		
		self.renderStats.eventHandlingTime = timer() - eventStart

		if self.health <= 0:
			Log("Health reached below zero.", LogLevel.Info, __name__)
			self.isRunning = False

		if self.health >= self.maxHealth:
			self.health = self.maxHealth

		if self.time_ms >= self.map.length:
			self.map.shouldPlay = False

		if not self.map.shouldPlay:
			Log("Map has ended.", LogLevel.Info, __name__)
			self.isRunning = False

		self.__UpdateCircles()

		self.renderStats.blitCount = self.pointsText.blitsRequired + self.comboText.blitsRequired + self.fpsCounter.blitsRequired + self.healthBar.blitsRequired + self.clicksText.blitsRequired
		for circle in self.map.objectsLeft:
			if circle.shouldDraw:
				self.renderStats.blitCount += 1

		self.renderStats.updateTime = timer() - updateStart
		self.renderStats.frameTime = self.renderStats.updateTime + self.renderStats.renderTime
		self.health -= HP * self.renderStats.updateTime * 79.2

	def Run(self):
		if not prefs.autoGenerate:
			Map.resolution = (self.width, self.height)
			self.map = Map('Resources/maps/test.txt')
		else:
			self.map = EmptyMap()
			self.GenerateRandomCircle()

		if self.map.loadSuccess == -1:
			Log("An error appeared during map loading.", LogLevel.Error, __name__)
			self.menu.AddMessage("An error appeared during map loading.")
			self.isRunning = False

		#free memory after map loading
		FreeMem('Started after map loading garbage collection.')

		self.renderThread.start()
		while self.isRunning:
			self.Update()
		
		self.renderThread.join()

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

		FreeMem("Started onclose garbage collection.")
							
	def DrawCursor(self):
		tex = mainResManager.GetTexture('cursor')
		self.win.blit(tex.Get(), (self.cursorPos[0] - tex.Width / 2, self.cursorPos[1] - tex.Height / 2))
		self.renderStats.blitCount += 1
	
	def DrawGui(self):
		self.comboText.Render(self.win, self.combo)
		self.healthBar.Render(self.win, self.health, self.maxHealth, self.time)
		self.pointsText.Render(self.win, self.points)
		self.clicksText.Render(self.win, self.clickCount[0], self.clickCount[1])
		if debug.ENABLE:
			if prefs.useNewFpsCounter:
				self.fpsCounter.Render(self.win, self.renderStats.frameTime, self.renderStats.renderTime, self.renderStats.updateTime, self.renderStats.eventHandlingTime, self.renderStats.playgroundDrawTime, self.renderStats.waitTime, self.renderStats.blitCount)
			else:
				self.fpsCounter.Render(self.win, self.renderStats.frameTime)