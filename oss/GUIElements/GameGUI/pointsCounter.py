import pygame

class PointsCounter(object):
	def __init__(self, basefont, pos, textColor=(184, 176, 160)):
		self.font = basefont
		self.pos = pos
		self.textColor = textColor

		self.InitTextBase()

	def InitTextBase(self):
		rBaseText = self.font.render("points: ", True, self.textColor)

		self.textSurf = pygame.Surface((rBaseText.get_width(), rBaseText.get_height()), pygame.SRCALPHA).convert()
		self.textSurf.set_colorkey((0, 0, 0))
		self.textSurf.blit(rBaseText, (0, 0))

	def Render(self, surf, points):
		rNumText = self.font.render(str(points), True, self.textColor)

		textPos = (self.pos[0] - self.textSurf.get_width() - rNumText.get_width() - 1, self.pos[1] - self.textSurf.get_height())
		numPos = (self.pos[0] - rNumText.get_width(), self.pos[1] - self.textSurf.get_height())

		surf.blit(self.textSurf, textPos)
		surf.blit(rNumText, numPos)
	
	@property
	def blitsRequired(self):
		return 2
		