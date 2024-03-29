if __name__ == "__main__":
	import sys
	sys.exit()

from Utils.graphics import Color
from launcher import mainResManager, prefs
from GUIElements.pygameButton import Button
from GUIElements.notification import Notification
from game import Game
from editor import Editor
from Utils.debug import Log, LogLevel

import pygame
import time

Button.LoadFont("default", mainResManager.MainFont)

class Menu():
	fadeOutDuration = 1.0

	def __init__(self, win):
		self.win = win
		self.width = win.get_width()
		self.height = win.get_height()
		self.game = None
		self.time = 0
		self.frameTime = 0
		self.cursorPos = (0, 0)
		self.isRunning = True
		self.messages = []

		self.startButton = Button((25, self.height - 80, 170, 32), (156, 45, 119), self.Start, "Start new game!")
		self.exitButton = Button((25, self.height - 40, 170, 32), (156, 45, 119), self.Close, "Exit")
		self.editorButton = Button((25, self.height - 120, 170, 32), (156, 45, 119), self.OpenEditor, "Maps editor")
		self.settingsButton = Button((25, 25, 48, 48), (0, 0, 0), self.OpenSettings, backgroundImg=mainResManager.GetTexture("setsIcn").Get())

		self.startButton.activeColor = Color.Gray
		self.exitButton.activeColor = Color.Gray
		self.editorButton.activeColor = Color.Gray

		self.startButton.colorOnHover = True
		self.exitButton.colorOnHover = True
		self.editorButton.colorOnHover = True

		self.AddMessage("Welcome to Oss!")
		pygame.display.set_caption("Oss! - Menu")

	def Run(self):
		while self.isRunning:
			start = time.perf_counter()
			for event in pygame.event.get(): 
				if event.type == pygame.MOUSEMOTION:
					self.cursorPos = pygame.mouse.get_pos()

				if event.type == pygame.QUIT:
					self.isRunning = False

				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						self.isRunning = False
					if event.key == prefs.keyBinds["savePreferencies"]:
						prefs.ExportToFile(prefs.PREFS_FILE)
						Log("Saved user settings.", LogLevel.Info, __name__)
						self.AddMessage("Saved user settings")

			self.startButton.Update()
			self.exitButton.Update()
			self.editorButton.Update()
			self.settingsButton.Update()

			if len(self.messages) != 0:
				self.messages[0].Update(self.frameTime)
				if self.messages[0].dispose:
					self.messages.remove(self.messages[0])

			if self.game:
				self.startButton.text = 'Game is currently running'
				self.startButton.activeColor = Color.Red
				self.startButton.inactiveColor = Color.Red

			self.DrawBackground()
			self.DrawButtons()
			self.DrawMessageBox()
			self.DrawCursor()
			pygame.display.flip()
			
			self.frameTime = time.perf_counter() - start
			self.time += self.frameTime
		
	def Close(self):
		self.isRunning = False

	def Start(self):
		Game.Start(self.win, self)

	def OpenEditor(self):
		Editor.Start(self.win, self)
	
	def OpenSettings(self):
		self.AddMessage("Not working yet...")
	
	def AddMessage(self, message):
		self.messages.append(Notification(pygame.Rect(205, self.height - 32, self.width - 205, 32), message, (128, 128, 128), (205, self.height + 32)))

	def DrawCursor(self):
		drawPos = (self.cursorPos[0] - mainResManager.GetTexture('cursor').Width / 2, self.cursorPos[1]- mainResManager.GetTexture('cursor').Height / 2)
		self.win.blit(mainResManager.GetTexture("cursor").Get(), drawPos)

	def DrawBackground(self):
		self.win.blit(mainResManager.GetTexture("menu_background").Get(), (0, 0))

	def DrawButtons(self):
		self.startButton.Render(self.win)
		self.exitButton.Render(self.win)
		self.editorButton.Render(self.win)
		self.settingsButton.Render(self.win)
	
	def DrawMessageBox(self):
		if len(self.messages) != 0:
			self.messages[0].Render(self.win)