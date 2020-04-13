if __name__ == '__main__':
	import sys
	sys.exit()

import pygame
from launcher import debugging, AR, HP, CS, mainResManager, LauncherInfo, prefs
from eventhandler import EventHandler
from Utils.memory import FreeMem
from Utils.graphics import Color
from Utils.game import Stats, GetPlayfield
import time
import random
from eventhandler import EventHandler
from GameElements.circle import Circle
from GameElements.map import Map, EmptyMap

#import cuncurrent.futures ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

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
		self.maxhealth = 100
		self.pointsColor = Color.Random()
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
		FreeMem(debugging, 'Started after-init garbage collection.')

	def Run(self):
		global debugging
		
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
			if LauncherInfo.timePerfCounterAvailable:
				start = time.perf_counter()
			else:
				start = time.time()
			
			self.events = pygame.event.get()

			#event handling
			for event in self.events: 
				if event.type == pygame.MOUSEMOTION:
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
			self.DrawPlayGround()
			if self.draw_interface:
				self.DrawCombo()
				self.DrawHealthBar()
				self.DrawPoints()
				self.DrawClicksCounter()
				if debugging:
					self.DrawFPSCounter()
			self.DrawCursor()

			pygame.display.flip()

			#calculate fps etc.
			if prefs.useFpsCap:
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

		FreeMem(debugging, 'Started onclose garbage collection.')

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
			if self.time_ms >= circle.startTime and self.time_ms <= circle.endTime:
				circle.Draw(self.win, self.time_ms)
						
				for event in self.events:
					if event.type == pygame.KEYDOWN:
						if event.key == prefs.keyBinds['kl'] or event.key == prefs.keyBinds['kr']:
							topCircle.Collide(self, self.cursorPos)

					if event.type == pygame.MOUSEBUTTONDOWN:
						EventHandler.HandleMouse(self, event)
						topCircle.Collide(self, self.cursorPos)
			elif self.time_ms > circle.endTime:
				topCircle.Miss(self)
							
	def DrawCursor(self):
		self.win.blit(mainResManager.GetTexture('cursor').Get(), (self.cursorPos[0] - mainResManager.GetTexture('cursor').Width / 2, self.cursorPos[1] - mainResManager.GetTexture('cursor').Height / 2))

	def DrawCombo(self):
		font = mainResManager.GetFont("comicsansms_48")

		rText = font.render('combo: {}'.format(self.combo), True, Color.White)

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
			c = Color.Red
		else:
			c = Color.Green

		pygame.draw.rect(self.win, Color.Gray, (pos, bgSize))
		pygame.draw.rect(self.win, c, (pos, barSize))

		font = mainResManager.GetFont("comicsansms_24")
		rText = font.render('Time: {}s'.format(round(self.time, 2)), True, Color.White)

		self.win.blit(rText, (barBgRect.x, barBgRect.centery - rText.get_height() / 2))

	def DrawClicksCounter(self):
		font = mainResManager.GetFont("comicsansms_24")
		rTextLeft = font.render(str(self.click_count[0]), True, Color.White)
		rTextRight = font.render(str(self.click_count[1]), True, Color.White)

		leftPos = (self.width - rTextLeft.get_width() - 3, self.height / 2 - rTextLeft.get_height() / 2)
		rightPos = (self.width - rTextRight.get_width() - 3, self.height / 2 + rTextRight.get_height() / 2)

		self.win.blit(rTextLeft, leftPos)
		self.win.blit(rTextRight, rightPos)

	def DrawFPSCounter(self):
		font = mainResManager.GetFont("comicsansms_12")
		text = 'Frame time: {}ms | FPS: {}'.format(round(self.frameTime * 1000, 3), round(self.fps, 3))
		rText = font.render(text, True, Color.White)
		pos = (int(self.width - 38 * 6), self.height - rText.get_height() - 2)

		self.win.blit(rText, pos)