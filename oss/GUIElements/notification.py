from .pygameText import Text
from .pygameButton import CloseButton
from Utils.graphics import IsFullyVisible, IsPartiallyVisible
from launcher import prefs
import pygame

class Notification:
	flyInDuration = 0.35
	flyOutDuration = 0.35

	class AnimationDirection:
		Up, Down, Left, Right = range(4)

	@staticmethod
	def Animate(animationDirection, step):
		changeX = changeY = 0

		if animationDirection == Notification.AnimationDirection.Up:
			changeX = 0
			changeY = -step
		elif animationDirection == Notification.AnimationDirection.Down:
			changeX = 0
			changeY = step
		elif animationDirection == Notification.AnimationDirection.Left:
			changeX = -step
			changeY = 0
		elif animationDirection == Notification.AnimationDirection.Right:
			changeX = step
			changeY = 0
		else:
			raise RuntimeError("Animation error: invalid Notification.AnimationDirection argument: {}".format(animationDirection))
		
		return (changeX, changeY)
	
	def __init__(self, rect, text, bgColor, startPos, textColor=(0, 0, 0)):
		self.msg = text
		self.rect = rect
		self.pos = list(startPos)
		self.closed = False
		self.dispose = False

		self.closeButton = CloseButton((rect.right - 12, rect.y + 2, 10, 10), (0, 0, 0, 255), self.Close)
		self.text = Text((0, 0, self.rect.width, self.rect.height), text, bgColor, textColor)

		self.drawSurf = pygame.Surface((rect.width, rect.height)).convert()
		self.text.Render(self.drawSurf)
		self.closeButton.Render(self.drawSurf, pos=(self.drawSurf.get_width() - 12, 2), size=(10, 10))
		self.drawSurf.set_alpha(185)
	
	def Render(self, surf):
		surf.blit(self.drawSurf, (int(self.pos[0]), int(self.pos[1])))

	def Update(self, time):
		tempRect = pygame.Rect(self.pos[0], self.pos[1], self.rect.width, self.rect.height)
		if not self.closed:
			if not IsFullyVisible(tempRect, prefs.resolution):
				change = Notification.Animate(Notification.AnimationDirection.Up, self.rect.height / Notification.flyInDuration * time)
				self.pos[0] += change[0]
				self.pos[1] += change[1]
			
			self.closeButton.Update()
		else:
			if IsPartiallyVisible(tempRect, prefs.resolution):
				change = Notification.Animate(Notification.AnimationDirection.Down, self.rect.height / Notification.flyOutDuration * time)
				self.pos[0] += change[0]
				self.pos[1] += change[1]
			else:
				self.dispose = True

	def Close(self):
		self.closed = True