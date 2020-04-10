if __name__ == '__main__':
	quit()

import pygame
pygame.font.init()

def RenderText(surf, text, initPos, font, color=(255, 255, 255)):
	raise NotImplementedError
	lines = text.splitlines()
	
	lineNo = 0
	for line in lines:
		text = font.render(line, True, color)
		surf.blit(text, (initPos[0], initPos[1] + text.get_height() * lineNo))
		lineNo += 1

class TextBox:
	FONTS = {
		"default": pygame.font.SysFont("comicsansms", 12)}

	@classmethod
	def LoadFont(cls, name, font):
		cls.FONTS[name] = font

	def __init__(self, rect, color, textColor, defaultText = ""):
		if isinstance(rect, pygame.Rect):
			self.rect = rect
		elif isinstance(rect, tuple):
			if len(rect) == 4:
				self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
			else:
				raise TypeError("Given list not valid (expected 4 elements, got {})".format(len(rect)))
		else:
			raise TypeError("Expected pygame.Rect object or tuple, got {}".format(type(rect)))

		self.text = ""
		self.boxActiveColor = self.boxInactiveColor = color
		self.textColor = textColor
		self.isActive = False
		self.defaultText = defaultText
		self.usedFont = "default"

		self.returnAction = None

	def Render(self, surf):
		if self.isActive:
			color = self.boxActiveColor
		else:
			color = self.boxInactiveColor

		pygame.draw.rect(surf, color, self.rect)

		rText = TextBox.FONTS[self.usedFont].render(self.text, True, self.textColor)
		surf.blit(rText, (self.rect.left + 2, self.rect.centery - rText.get_height() / 2))

	def Clear(self):
		self.text = defaultText
		self.isActive = False

	def Collide(self, pos):
		if self.rect.collidepoint(pos):
			self.isActive = True

			if self.text == self.defaultText:
				self.text = ""
		else:
			self.isActive = False

	def Update(self, event):
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				pos = pygame.mouse.get_pos()

				self.Collide(pos)

		if self.isActive:
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if self.returnAction:
						self.returnAction()
					self.text = ""
				elif event.key == pygame.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode

		if not self.isActive:
			self.text = self.defaultText