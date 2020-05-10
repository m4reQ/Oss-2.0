import pygame

class FpsCounter(object):
	def __init__(self, baseFont, pos, textColor=(255, 255, 255), textColor2=(255, 255, 0)):
		self.font = baseFont
		self.pos = pos

		self.textColor = textColor
		self.textColor2 = textColor2
	
	def Render(self, surf, profiling, frameTime):
		text = 'Frame time: {0:.2f}ms'.format(frameTime * 1000)
		rText = self.font.render(text, True, self.textColor)
		pos = (self.pos[0] - rText.get_width(), self.pos[1] - rText.get_height())

		if profiling:
			rProfilingText = self.font.render("[PROFILING]", True, self.textColor2)
			surf.blit(rProfilingText, (pos[0] - rProfilingText.get_width(), pos[1]))

		surf.blit(rText, pos)
	
	@property
	def blitsRequired(self):
		return 1

class NewStyleFpsCounter(object):
	def __init__(self, baseFont, pos, size, textColor1=(255, 255, 255), textColor2=(128, 128, 128), textColor3=(255, 255, 0)):
		self.font = baseFont
		self.pos = pos

		self.baseTextColor = textColor1
		self.blitsTextColor = textColor2
		self.profilingTextColor = textColor3

		self.surfWidth = size[0]
		self.surfHeight = size[1]
		self.textBaseOffset = int(self.surfWidth / 1.5)

		self.textSurface = pygame.Surface((self.textBaseOffset, self.surfHeight), pygame.SRCALPHA).convert()
		self.textSurface.set_colorkey((0, 0, 0))

		self.InitTextBase()
	
	def InitTextBase(self):
		textOffset = 0

		self.font.set_bold(True)
		rBaseFrameText = self.font.render("FrameTime: ", True, self.baseTextColor)
		self.font.set_bold(False)
		rBaseRenderText = self.font.render("Render: ", True, self.baseTextColor)
		rBaseUpdateText = self.font.render("Update: ", True, self.baseTextColor)
		rBaseEventText = self.font.render("Event: ", True, self.baseTextColor)
		rBasePlaygroundText = self.font.render("Circles render: ", True, self.baseTextColor)
		rBaseWaitText = self.font.render("Wait time: ", True, self.baseTextColor)
		rBaseBlitsText = self.font.render("Blits: ", True, self.blitsTextColor)

		self.textSurface.blit(rBaseFrameText, (0, textOffset))
		textOffset += rBaseFrameText.get_height() + 1
		self.textSurface.blit(rBaseRenderText, (0, textOffset))
		textOffset += rBaseRenderText.get_height() + 1
		self.textSurface.blit(rBaseUpdateText, (0, textOffset))
		textOffset += rBaseUpdateText.get_height() + 1
		self.textSurface.blit(rBaseEventText, (0, textOffset))
		textOffset += rBaseEventText.get_height() + 1
		self.textSurface.blit(rBasePlaygroundText, (0, textOffset))
		textOffset += rBasePlaygroundText.get_height() + 1
		self.textSurface.blit(rBaseWaitText, (0, textOffset))
		textOffset += rBaseWaitText.get_height() + 1
		self.textSurface.blit(rBaseBlitsText, (0, textOffset))
		textOffset += rBaseBlitsText.get_height() + 1

	def Render(self, surf, profiling, frameTime, renderTime, updateTime, eventTime, playgroundTime, waitTime, blitsCount):
		textOffset = 0

		frameText = "{0:.2f}ms".format(frameTime * 1000)
		renderText = "{0:.2f}ms".format(renderTime * 1000)
		updateText = "{0:.2f}ms".format(updateTime * 1000)
		eventText = "{0:.2f}ms".format(eventTime * 1000)
		playgroundText = "{0:.2f}ms".format(playgroundTime * 1000)
		waitText = "{0:.2f}ms".format(waitTime * 1000)
		blitsText = "{}".format(blitsCount)

		self.font.set_bold(True)
		rFrameText = self.font.render(frameText, True, self.baseTextColor)
		self.font.set_bold(False)
		rRenderText = self.font.render(renderText, True, self.baseTextColor)
		rUpdateText = self.font.render(updateText, True, self.baseTextColor)
		rEventText = self.font.render(eventText, True, self.baseTextColor)
		rPlaygroundText = self.font.render(playgroundText, True, self.baseTextColor)
		rWaitText = self.font.render(waitText, True, self.baseTextColor)
		rBlitsText = self.font.render(blitsText, True, self.blitsTextColor)
		
		numberSurface = pygame.Surface((int(self.surfWidth - self.textSurface.get_width()), self.surfHeight), pygame.SRCALPHA).convert()
		numberSurface.set_colorkey((0, 0, 0))

		numberSurface.blit(rFrameText, (0, textOffset))
		textOffset += rFrameText.get_height() + 1
		numberSurface.blit(rRenderText, (0, textOffset))
		textOffset += rRenderText.get_height() + 1
		numberSurface.blit(rUpdateText, (0, textOffset))
		textOffset += rUpdateText.get_height() + 1
		numberSurface.blit(rEventText, (0, textOffset))
		textOffset += rEventText.get_height() + 1
		numberSurface.blit(rPlaygroundText, (0, textOffset))
		textOffset += rPlaygroundText.get_height() + 1
		numberSurface.blit(rWaitText, (0, textOffset))
		textOffset += rWaitText.get_height() + 1
		numberSurface.blit(rBlitsText, (0, textOffset))
		textOffset += rBlitsText.get_height() + 1
		
		if profiling:
			self.font.set_bold(True)
			rText = self.font.render("[PROFILING]", True, self.profilingTextColor)
			self.font.set_bold(False)
			surf.blit(rText, (self.pos[0] - int(self.surfWidth / 2) - int(rText.get_width() / 2), self.pos[1] + textOffset))

		surf.blit(self.textSurface, (self.pos[0] - self.surfWidth, self.pos[1]))
		surf.blit(numberSurface, (self.pos[0] - self.surfWidth + self.textSurface.get_width(), self.pos[1]))
	
	@property
	def blitsRequired(self):
		return 2