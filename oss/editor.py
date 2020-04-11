if __name__ == "__main__":
	import sys
	sys.exit()

try:
	import pygame
	from helper import logError, exitAll
	from utils import FreeMem, GetPlayfield, color, translateCoord, TranslationMode
	import concurrent.futures
	from launcher import debugging, mapsPath, CS, mainResManager, prefs
	import time
except ImportError as e:
	logError(e)
	exitAll()

#register files
TIME_FILE = open(mapsPath + "editor/time.txt", 'w+')
POS_FILE = open(mapsPath + "editor/position.txt", 'w+')

class RegisterMode():
	Time, Position = range(2)

class Editor:
	regMode = RegisterMode.Position

	@classmethod
	def Start(cls, win, menu):
		inst = cls(win, menu)
		menu.game = inst
		inst.Run()
	
	def __init__(self, parentWin, menu):
		self.width = parentWin.get_width()
		self.height = parentWin.get_height()
		self.win = parentWin
		self.menu = menu
		self.isRunning = True
		self.cursorPos = (0, 0)
		self.playfield = GetPlayfield(self.width, self.height, CS)
		self.lastRegs = [(0, 0), (0, 0)]
		self.time = 0
		self.objCount = 0

		pygame.display.set_caption("Oss! - Editor")

	def Run(self):
		while self.isRunning:
			start = time.time()
			#update
			for event in pygame.event.get():
				if event.type == pygame.MOUSEMOTION:
					self.cursorPos = pygame.mouse.get_pos()
				
				if event.type == pygame.QUIT:
					self.isRunning = False
				
				if event.type == pygame.KEYDOWN:
					if event.key == prefs.keyBinds["kl"] or event.key == prefs.keyBinds["kr"]:
						if self.cursorPos[0] >= self.playfield["minX"] and self.cursorPos[0] <= self.playfield["maxX"] and self.cursorPos[1] >= self.playfield["minY"] and self.cursorPos[1] <= self.playfield["maxY"]:
								self.Click()
					
					if event.key == pygame.K_ESCAPE:
						self.isRunning = False
					
					if event.key == pygame.K_m:
						Editor.regMode = RegisterMode.Position if Editor.regMode == RegisterMode.Time else RegisterMode.Time

			#render 
			self.Render()

			pygame.display.flip()
			time.sleep(1.0 / 60.0)

			self.time += time.time() - start
		
		self.Close()
	
	def Close(self):
		POS_FILE.close()
		TIME_FILE.close()
		self.menu.game = None
		FreeMem(debugging, 'Started onclose garbage collection.')
	
	def Render(self):
		#clear
		self.win.fill((110, 33, 84))

		#render playfield
		playField = pygame.Rect(self.playfield["minX"], self.playfield["minY"], self.playfield["width"], self.playfield["height"])
		pygame.draw.rect(self.win, (0, 0, 0), playField, 1)

		#render points
		pygame.draw.circle(self.win, color.red, self.lastRegs[0], 3)
		pygame.draw.circle(self.win, color.green, self.lastRegs[1], 3)

		#render mode
		if Editor.regMode == RegisterMode.Time:
			mode = "Time"
		elif Editor.regMode == RegisterMode.Position:
			mode = "Position"
		else:
			mode = "Invalid"

		rModeText = mainResManager.GetFont("comicsansms_18").render("Register mode: {}".format(mode), True, color.white)
		self.win.blit(rModeText, (3, 3))

		#render time
		rTimeText = mainResManager.GetFont("comicsansms_24").render("Time: {}ms".format(int(self.time * 1000)), True, color.white)
		self.win.blit(rTimeText, (3, rModeText.get_height() + 3))
		
		#render cursor
		self.win.blit(mainResManager.GetTexture('cursor').Get(), (self.cursorPos[0] - mainResManager.GetTexture('cursor').Width / 2, self.cursorPos[1] - mainResManager.GetTexture('cursor').Height / 2))
	
	def Click(self):
		if debugging:
			print('[INFO]<{}>Last registered: {}, {}'.format(__name__, self.time, self.cursorPos))

		if Editor.regMode == RegisterMode.Time:
			TIME_FILE.write("{}. object at time: {}\n".format(self.objCount, self.time))
			self.objCount += 1
		elif Editor.regMode == RegisterMode.Position:
			tPos = translateCoord(self.cursorPos, (self.width, self.height), TranslationMode.Encode)
			POS_FILE.write("{}. object at position: {}, {}\n".format(self.objCount, tPos[0], tPos[1]))
			lastReg = self.cursorPos

			self.lastRegs[0], self.lastRegs[1] = self.lastRegs[1], lastReg

			self.objCount += 1
		else:
			print('Wrong register mode! Changing register mode to "time".')
			Editor.regMode = RegisterMode.Time