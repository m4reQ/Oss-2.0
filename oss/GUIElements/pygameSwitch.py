if __name__ == '__main__':
	quit()

import pygame
pygame.font.init()

class Switch:
	CheckTreshold = 60

	def __init__(self, rect, color, onClickFunc, backgroundImg = None):
		if isinstance(rect, pygame.Rect):
			self.rect = rect
		elif isinstance(rect, tuple):
			if len(rect) == 4:
				self.rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])
			else:
				raise TypeError("Given list not valid (expected 4 elements, got {})".format(len(rect)))
		else:
			raise TypeError("Expected pygame.Rect object or tuple, got {}".format(type(rect)))

		self.color = self.inactiveColor = self.activeColor = color
		self.onClickFunc = onClickFunc

		self.backgroundImg = backgroundImg
		if backgroundImg:
			self.coloredImg = backgroundImg.copy()
			self.coloredImg.fill((self.color[0], self.color[1], self.color[2], 0), None, pygame.BLEND_RGBA_SUB)
		else:
			self.coloredImg = backgroundImg

		self.activeImg = backgroundImg

		self.__state = False
		self.__previousState = False

		self.__colored = False

		self.__checksPerformed = 0

		self.__shouldCheck = True

	def Render(self, surf):
		if self.backgroundImg:
			surf.blit(self.activeImg, (self.rect.x, self.rect.y))
		else:
			pygame.draw.rect(surf, self.activeColor, self.rect)

	def Update(self):
		if not self.__shouldCheck:
			self.__checksPerformed += 1
			if self.__checksPerformed >= Switch.CheckTreshold:
				self.__checksPerformed = 0
				self.__shouldCheck = True

			return

		pos = pygame.mouse.get_pos()

		if pygame.mouse.get_pressed()[0]:
			if self.Collide(pos):
				self.__state = not self.__state

		if self.onClickFunc and self.__state != self.__previousState:
			self.onClickFunc()
		
		if self.__state:
			self.activeImg = self.coloredImg
		else:
			self.activeImg = self.backgroundImg

		if self.__state:
			self.activeColor = self.color
		else:
			self.activeColor = self.inactiveColor

		if self.__state != self.__previousState:
			self.__shouldCheck = False

		self.__previousState = self.__state
	
	def Collide(self, pos):
		return self.rect.collidepoint(pos)
	
	@property
	def StateChanged(self):
		return self.__state != self.__previousState

	@property
	def State(self):
		return self.__state