class ClicksCounter(object):
	def __init__(self, basefont, pos, textColor=(161, 160, 157)):
		self.font = basefont
		self.pos = pos
		self.textColor = textColor
	
	def Render(self, surf, leftClicks, rightClicks):
		rTextLeft = self.font.render(str(leftClicks), True, self.textColor)
		rTextRight = self.font.render(str(rightClicks), True, self.textColor)

		lPos = (self.pos[0] - rTextLeft.get_width(), self.pos[1] - rTextLeft.get_height() - 1)
		rPos = (self.pos[0] - rTextRight.get_width(), self.pos[1] + 1)

		surf.blit(rTextLeft, lPos)
		surf.blit(rTextRight, rPos)

	@property
	def blitsRequired(self):
		return 2