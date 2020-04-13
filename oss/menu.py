if __name__ == "__main__":
	import sys
	sys.exit()

try:
	from helper import exitAll, logError
	from Utils.graphics import Color
	from launcher import mainResManager, LauncherInfo, prefs, debugging
	from GUIElements.pygameButton import Button
	from GUIElements.notification import Notification
	import time
	from game import Game
	import pygame
	from editor import Editor
except ImportError:
	print("Cannot load menu.")
	raise

#import concurrent module ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

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

		self.startButton.activeColor = Color.Gray
		self.exitButton.activeColor = Color.Gray
		self.editorButton.activeColor = Color.Gray

		self.startButton.colorOnHover = True
		self.exitButton.colorOnHover = True
		self.editorButton.colorOnHover = True

		pygame.display.set_caption("Oss! - Menu")

	def Run(self):
		while self.isRunning:
			#event handling
			start = time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time()
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
						if debugging:
							print("[INFO]<{}> Saved user settings.".format(__name__))
							self.AddMessage("Saved user settings")	
					if event.key == prefs.keyBinds["debugGetPos"] and debugging:
						pos = pygame.mouse.get_pos()
						print('[INFO]<{}> Current mouse position: {}, mapped coords (current resolution): {}'.format(__name__, pos, (pos[0] / self.width, pos[1] / self.height)))
					if event.key == prefs.keyBinds["debugUpdateWindow"] and debugging:
						pygame.display.flip()

			#update
			self.startButton.Update()
			self.exitButton.Update()
			self.editorButton.Update()
			for msg in self.messages:
				msg.Update(self.frameTime)
				if msg.dispose:
					self.messages.remove(msg)

			if self.game:
				self.startButton.text = 'Game is currently running'
				self.startButton.activeColor = Color.Red
				self.startButton.inactiveColor = Color.Red

			#render
			self.DrawBackground()
			self.DrawButtons()
			self.DrawMessageBox()
			self.DrawCursor()
			pygame.display.flip()
			
			end = time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time()
			self.frameTime = end - start
			self.time += self.frameTime
		
	def Close(self):
		self.isRunning = False

	def Start(self):
		Game.Start(self.win, self)

	def OpenEditor(self):
		Editor.Start(self.win, self)
	
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
	
	def DrawMessageBox(self):
		if len(self.messages) != 0:
			self.messages[0].Render(self.win)