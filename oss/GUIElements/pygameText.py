if __name__ == '__main__':
	quit()

import pygame
pygame.font.init()

class Text:
	FONTS = {
		"default": pygame.font.SysFont("comicsansms", 12)}

	@classmethod
	def LoadFont(cls, name, font):
		cls.FONTS[name] = font

	def __init__(self, rect, text, bgColor=None, textColor=(255, 255, 255)):
		if isinstance(rect, pygame.Rect):
			self.rect = rect
		elif isinstance(rect, tuple):
			if len(rect) == 4:
				self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
			else:
				raise TypeError(f"Given list not valid (expected 4 elements, got {len(rect)})")
		else:
			raise TypeError(f"Expected pygame.Rect object or tuple, got {type(rect)}")

		self.bgColor = bgColor
		self.text = text
		self.textColor = textColor
		self.drawSurface = pygame.Surface((self.rect.width, self.rect.height))
		self.usedFont = "default"

	def Render(self, surf):
		if self.bgColor:
			if len(self.bgColor) == 4:
				self.drawSurface.set_alpha(self.bgColor[3])
			self.drawSurface.fill(self.bgColor[0:3])

			surf.blit(self.drawSurface, (self.rect.x, self.rect.y))

		rText = Text.FONTS[self.usedFont].render(self.text, True, self.textColor)

		surf.blit(rText, (self.rect.centerx - rText.get_width() / 2, self.rect.centery - rText.get_height() / 2))