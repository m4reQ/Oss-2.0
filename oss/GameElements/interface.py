from utils import run_once
import utils
import helper
import pygame

debugging = False

def SetDebugging(val):
	"""
	sets debugging mode to given value
	rtype: bool
	returns: None
	"""
	global debugging
	debugging = val

class Rect(object):
	def __init__(self, position, width, height, color=None, text=None, textPosition=None):
		if not textPosition and text:
			self.textPosition = position
		else:
			self.textPosition = textPosition

		if not color:
			self.color = utils.color.black
		else:
			self.color = color

		self.width = width
		self.height = height
		self.posX, self.posY = position
	
	def Return(self):
		return 

class InterfaceElement:
	font = None

	def __init__(self, width, height, position, image=None, rect=None, text=None, color=None, textColor=None, textPosition=None):
		if debugging:
			if not InterfaceElement.font:
				print('[WARNING]', str(self), ' Font not defined.')
			if text and not textColor:
				print('[WARNING]', str(self), ' Text color not defined.')

		self.positionX, self.positionY = position
		self.width = width
		self.height = height

		self.image = image
		self.rect = rect
		self.text = text

		self.font = InterfaceElement.font

		if not color:
			self.color = utils.color.black
		else:
			self.color = color

		if not textColor:
			self.textColor = self.color
		else:
			self.textColor = textColor

		if not textPosition:
			self.textPositionX, self.textPositionY = position
		else:
			self.textPositionX, self.textPositionY = textPosition

	def Render(self, surface):
		#render text
		if self.text:
			rText = self.font.render(self.text, True, self.textColor)

		#check what elements are available
		if self.image and not self.text and not self.rect:
			surface.blit(self.image, (self.positionX, self.positionY))
		elif self.image and self.text and not self.rect:
			surface.blit(self.image, (self.positionX, self.positionY))
			surface.blit(rText, (self.textPositionX, self.textPositionY))
		elif not self.image and self.text and not self.rect:
			surface.blit(rText, (self.textPositionX, self.textPositionY))
		elif not self.image and not self.text and self.rect:
			pygame.draw.rect(surface, self.color, self.rect)
		elif not self.image and self.text and self.rect:
			pygame.draw.rect(surface, self.color, self.rect)
			surface.blit(rText, (self.textPositionX, self.textPositionY))
		else:
			if debugging:
				print('[WARNING]', str(self), ' No drawable set matches conditions. Skipping render.')
			pass

	def getRect(self):
		rect = pygame.Rect(self.positionX, self.positionY, self.width, self.height)

		return rect

def changeFont(fontName, size):
	InterfaceElement.font = pygame.font.SysFont(fontName, int(size))

if __name__ == '__main__':
	pygame.quit()
	quit()