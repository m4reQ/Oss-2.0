from helper import color, run_once
from game import DEBUG_MODE
import pygame
import pygame.locals

class InterfaceElement:
	font = None

	def __init__(self, width, height, position=(0,0), drawable=None, text=None, textColor=None, textPosition=None):
		if DEBUG_MODE:
			if not InterfaceElement.font:
				print('[WARNING]' + str(self) + ' Font not defined.')
			if text and not textColor:
				print('[WARNING]' + str(self) + ' Text color not defined.')
			if not drawable and not text:
				print("[WARNING]" + str(self) + " Didn't define any object to draw.")

		self.positionX, positionY = position
		self.width = width
		self.height = height
		self.drawable = drawable

		self.text = text
		self.font = InterfaceElement.font
		self.textColor = textColor

		if not textPosition:
			self.textPositionX, self.textPositionY = position
		else:
			self.textPositionX, self.textPositionY = textPosition

	def render(self, surface):
		if self.text:
			r_text = self.font.render(self.text, True, self.textColor)

			if self.drawable:
				surface.blit(self.drawable, (self.positionX, self.positionY))
			surface.blit(r_text, (self.textPositionX, self.textPositionY))
		if self.drawable:
			surface.blit(self.drawable, (self.positionX, self.positionY))
		else:
			raise Exception('[ERROR] No object to draw.')

	def getRect(self):
		if self.text and not self.drawable:
			rect = pygame.Rect((self.textPositionX, self.textPositionY), (self.width, self.height))
		else:
			rect = pygame.Rect((self.positionX, self.positionY), (self.width, self.height))

		return rect

def changeFont(fontName, size):
	InterfaceElement.font = pygame.font.SysFont(fontName, int(size))

if __name__ == '__main__':
	pygame.quit()
	quit()