if __name__ == '__main__':
	quit()

try:
	from helper import exitAll, logError
	from utils import color, translateCoord, FreeMem
	from launcher import mainResManager
	from launcher import LauncherInfo
	from launcher import sets
	from GUIElements.pygameButton import Button
	import time
	from game import Game
	import pygame
	from eventhandler import EventHandler
except Exception as e:
	print(e)
	logError(e)
	exitAll()

#import concurrent module ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

Button.LoadFont("default", mainResManager.MainFont)

class Menu():
	def __init__(self, win):
		self.win = win
		self.width = win.get_width()
		self.height = win.get_height()
		self.game = None
		self.time = 0
		self.cursorPos = (0, 0)
		self.isRunning = True

		self.startButton = Button((25, self.height - 80, 170, 32), (0, 215, 48), self.Start, "Start new game!")
		self.exitButton = Button((25, self.height - 40, 170, 32), (0, 215, 48), self.Close, "Exit")

		self.startButton.activeColor = color.gray
		self.exitButton.activeColor = color.gray

		self.startButton.colorOnHover = True
		self.exitButton.colorOnHover = True

		pygame.display.set_caption("Oss! - Menu")

	def Render(self):
		self.DrawBackground()
		self.DrawButtons()
		self.DrawCursor()

	def RenderConcurrently(self):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.submit(self.DrawBackground)
			executor.submit(self.DrawButtons)
			executor.submit(self.DrawCursor)

	def Run(self):
		while self.isRunning:
			#event handling
			start = time.time()
			for event in pygame.event.get(): 
				self.cursorPos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					EventHandler.HandleKeys(self, event)
				EventHandler.HandleEvents(self, event)

			self.startButton.Update()
			self.exitButton.Update()

			if self.game:
				self.startButton.text = 'Game is currently running'
				self.startButton.activeColor = color.red
				self.startButton.inactiveColor = color.red

			#render
			if LauncherInfo.concurrencyAvailable: self.RenderConcurrently()
			else: self.Render()

			#update
			pygame.display.flip()
			
			#always use vsync here because going on higher frame rate is unnecessary
			time.sleep(1.0 / 60.0)
			self.time += time.time() - start
		
	def Close(self):
		self.isRunning = False

	def Start(self):
		self.game = Game(self.win, self)
		self.game.Run()

		if self.game:
			self.startButton.color = (64, 64, 64)

	def DrawCursor(self):
		drawPos = (self.cursorPos[0] - mainResManager.GetTexture('cursor').Width / 2, self.cursorPos[1]- mainResManager.GetTexture('cursor').Height / 2)
		self.win.blit(mainResManager.GetTexture("cursor").Get(), drawPos)

	def DrawBackground(self):
		self.win.blit(mainResManager.GetTexture("menu_background").Get(), (0, 0))

	def DrawButtons(self):
		self.startButton.Render(self.win)
		self.exitButton.Render(self.win)