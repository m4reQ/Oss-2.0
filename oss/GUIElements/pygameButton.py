if __name__ == '__main__':
	quit()

import pygame
pygame.font.init()

class Button:
	FONTS = {
		"default": pygame.font.SysFont("comicsansms", 12)}

	@classmethod
	def LoadFont(cls, name, font):
		cls.FONTS[name] = font

	def __init__(self, rect, color, onClickFunc, text="", textColor=(255, 255, 255)):
		if isinstance(rect, pygame.Rect):
			self.rect = rect
		elif isinstance(rect, tuple):
			if len(rect) == 4:
				self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
			else:
				raise TypeError("Given list not valid (expected 4 elements, got {})".format(len(rect)))
		else:
			raise TypeError("Expected pygame.Rect object or tuple, got {}".format(type(rect)))

		self.color = self.activeColor = self.inactiveColor = color
		self.onClickFunc = onClickFunc

		self.text = text
		self.textColor = textColor
		self.usedFont = "default"
		self.textCentered = True

		self.colorOnHover = False

		self.__state = False
		self.__previousState = False
		self.__hoverState = False
		self.__previousHoverState = False

	def Render(self, surf):
		pygame.draw.rect(surf, self.color, self.rect)
		rText = Button.FONTS[self.usedFont].render(self.text, True, self.textColor)

		if self.textCentered:
			pos = (self.rect.centerx - rText.get_width() / 2, self.rect.centery - rText.get_height() / 2)
		else:
			pos = (self.rect.left, self.rect.centery - rText.get_height() / 2)

		surf.blit(rText, pos)

	def Update(self):
		self.color = self.inactiveColor

		pos = pygame.mouse.get_pos()

		if self.Collide(pos):
			self.__hoverState = True
		else:
			self.__hoverState = False

		if pygame.mouse.get_pressed()[0]:
			if self.Collide(pos):
				self.color = self.activeColor
				self.__state = True
			else:
				self.__state = False
		
		if self.colorOnHover:
			if self.__hoverState:
				self.color = self.activeColor
			else:
				self.color = self.inactiveColor

		if self.onClickFunc and self.__state != self.__previousState and self.__state:
			self.onClickFunc()

		self.__previousState = self.__state
		self.__state = False

		self.__previousHoverState = self.__hoverState
		self.__hoverState = False
	
	def Collide(self, pos):
		return self.rect.collidepoint(pos)
	
	@property
	def StateChanged(self):
		return self.__state != self.__previousState
	
	@property
	def HoverStateChanged(self):
		return self.__hoverState != self.__previousHoverState

class CloseButton(Button):
	def __init__(self, rect, color, onClickFunc):
		super().__init__(rect, color, onClickFunc)

		self.__state = False
		self.__previousState = False
		self.__hoverState = False
		self.__previousHoverState = False
	
	def Render(self, surf, pos=None, size=None):
		if pos and size:
			pygame.draw.aaline(surf, self.color, pos, (pos[0] + size[0], pos[1] + size[1]))
			pygame.draw.aaline(surf, self.color, (pos[0], pos[1] + size[1]), (pos[0] + size[0], pos[1]))
		else:
			pygame.draw.aaline(surf, self.color, (self.rect.x, self.rect.y), (self.rect.x + self.rect.width, self.rect.y + self.rect.height))
			pygame.draw.aaline(surf, self.color, (self.rect.x, self.rect.y + self.rect.width), (self.rect.x + self.rect.width, self.rect.y))
	
	def Update(self):
		pos = pygame.mouse.get_pos()

		if self.Collide(pos):
			self.__hoverState = True
		else:
			self.__hoverState = False

		if pygame.mouse.get_pressed()[0]:
			if self.Collide(pos):
				self.__state = True
			else:
				self.__state = False

		if self.onClickFunc and self.__state != self.__previousState and self.__state:
			self.onClickFunc()