try:
	from helper import exitAll, logError
	from utils import color, translateCoord, FreeMem
	from launcher import backgroundTextures, interfaceTextures
	from launcher import LauncherInfo
	from launcher import sets
	from game import Game
	import pygame
	from eventhandler import EventHandler
	import GameElements.interface as interface
	from os import system
except Exception as e:
	print(e)
	logError(e)
	exitAll()

#import concurrent module ONLY if it's available
if LauncherInfo.concurrencyAvailable:
	import concurrent.futures

#textures
bg_texture = backgroundTextures.GetTexture('menu_background')
cursor_texture = interfaceTextures.GetTexture('cursor')

class Menu():
	def __init__(self, win):
		self.clock = pygame.time.Clock()
		self.win = win
		self.width = win.get_width()
		self.height = win.get_height()
		self.game = None
		self.time = 0
		self.events = pygame.event.get()
		self.cursor_pos = (0, 0)
		self.is_running = True

		interface.changeFont('comicsansms', 24)

		self.cursor = interface.InterfaceElement(cursor_texture.get_width(), cursor_texture.get_height(), self.cursor_pos, image=cursor_texture)
		startButtonPos = translateCoord((0.62, 0.88), (self.width, self.height), 1)
		self.startButton = interface.InterfaceElement(180, 30, startButtonPos, rect=pygame.Rect(startButtonPos, (180, 30)), text='Start new game', textPosition=(startButtonPos[0]+2, startButtonPos[1]-6), textColor=color.white, color=color.green)
		exitButtonPos = translateCoord((0.025 ,0.88), (self.width, self.height), 1)
		self.exitButton = interface.InterfaceElement(180, 30, exitButtonPos, rect=pygame.Rect(exitButtonPos, (180, 30)), text='Exit.', textPosition=(exitButtonPos[0] + 60, exitButtonPos[1]-6), color=color.green, textColor=color.white)

	def Render(self):
		self.DrawMenu()
		self.DrawCursor()

	def RenderConcurrently(self):
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.submit(self.DrawMenu)
			executor.submit(self.DrawCursor)

	def Run(self):
		while self.is_running:
			self.events = pygame.event.get()

			#event handling
			for event in self.events: 
				self.cursor_pos = pygame.mouse.get_pos()

				if event.type == pygame.KEYDOWN:
					EventHandler.HandleKeys(self, event)

				EventHandler.HandleEvents(self, event)

				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:
						if self.startButton.getRect().collidepoint(self.cursor_pos):
							self.Start()
						if self.exitButton.getRect().collidepoint(self.cursor_pos):
							self.is_running = False

			#render
			if LauncherInfo.concurrencyAvailable: self.RenderConcurrently()
			else: self.Render()

			#update
			pygame.display.flip()
			
			#always use vsync here because going on higher frame rate is unnecessary
			self.clock.tick(60)

			self.time = pygame.time.get_ticks()
		
		self.Close()

	def Close(self):
		print('Goodbye!')
		if sets.DEBUG_MODE:
			print('[INFO]<{}> Program exited after: {} seconds.'.format(__name__, self.time))
		
		pygame.mixer.quit()
		pygame.quit()

		FreeMem(sets.DEBUG_MODE)
		
		system('pause >NUL')
		quit()

	def DrawCursor(self):
		self.cursor.positionX = self.cursor_pos[0] - self.cursor.width/2
		self.cursor.positionY = self.cursor_pos[1] - self.cursor.height/2

		self.cursor.Render(self.win)

	def Start(self):
		self.game = Game(self.win, self)

		self.game.Run()

	def DrawMenu(self):
		self.win.blit(bg_texture, (0, 0))

		if self.game:
			interface.changeFont('comicsansms', 12)
			self.startButton.text = 'Game is currently running'
			self.startButton.color = color.red

		self.startButton.Render(self.win)

		self.exitButton.Render(self.win)

if __name__ == '__main__':
	exitAll()