if __name__ == "__main__":
	import sys
	sys.exit()

import pygame
import time
import sys

class WindowFlags:
	NoFlags = 0
	FullScreen = pygame.FULLSCREEN
	DoubleBuf = pygame.DOUBLEBUF
	Accelerated = pygame.HWSURFACE | pygame.HWACCEL
	BorderLess = pygame.NOFRAME
	Resizable = pygame.RESIZABLE

def GetColorDepth(width, height):
	return pygame.display.mode_ok((width, height))

def CreateWindow(width, height, title, flags):
	if not pygame.get_init():
		pygame.init()

	colorDepth = GetColorDepth(width, height)

	try:
		win = pygame.display.set_mode((width, height), flags, colorDepth)
	except pygame.error:
		raise Exception("Cannot create window.")

	pygame.display.set_caption(title)

	return win

class Window:
	def __init__(self, width, height, title, flags, vSync = False, debug = False):
		self._mainFrame = CreateWindow(width, height, title, flags)
		self.renderSurface = pygame.Surface((width, height), pygame.HWSURFACE)

		self.width = width
		self.height = height
		self.baseTitle = title

		self.vSync = vSync
		self.debug = debug
		self.flags = flags

		self.events = []

		self.clearColor = (0, 0, 0)

		self.isRunning = True

		self.fps = 0.0
		self.frameTime = 0.0

	def MainLoop(self):
		while self.isRunning:
			start = time.perf_counter()

			self._DefaultUpdate()
			self.Update()
			if pygame.display.get_active():
				self.renderSurface.fill(self.clearColor)
				self.Render()
				self._PostRender()

			pygame.display.flip()

			if self.vSync:
				time.sleep(1.0 / 60.0)

			self.frameTime = time.perf_counter() - start
			self.fps = 1.0 / self.frameTime

		self.Close()

	def Close(self):
		pygame.quit()
		sys.exit()

	def _HardClose(self):
		sys.exit()

	def Resize(self, width, height):
		self.width = width
		self.height = height

		self._mainFrame = pygame.display.set_mode((width, height), self.flags, GetColorDepth(self.width, self.height))

	def Render(self):
		try:
			pygame.draw.rect(self.renderSurface, (255, 0, 0), pygame.Rect(10, 10, 10, 10))
		except Exception as e:
			if self.debug:
				print("[RENDER ERROR] " + str(e))

				self._HardClose()

	def _PostRender(self):
		try:
			self._mainFrame.blit(pygame.transform.scale(self.renderSurface, (self.width, self.height)), (0, 0))

		except Exception as e:
			if self.debug:
				print("[POST-RENDER ERROR] " + str(e))

				self._HardClose()

	def _DefaultUpdate(self):
		try:
			self.events = pygame.event.get()
			for event in self.events:
				if event.type == pygame.QUIT:
					self.isRunning = False
				if event.type == pygame.VIDEORESIZE:
					self.Resize(event.w, event.h)
		except Exception as e:
			if self.debug:
				print("[UPDATE ERROR] " + str(e))

				self._HardClose()

	def Update(self):
		try:
			if self.debug:
				pygame.display.set_caption(self.baseTitle + " | FPS: " + str(round(self.fps, 3)))
		except Exception as e:
			if self.debug:
				print("[UPDATE ERROR] " + str(e))

				self._HardClose()
