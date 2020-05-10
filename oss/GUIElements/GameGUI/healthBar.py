import pygame

class HealthBar(object):
	def __init__(self, basefont, pos, size, textColor=(255, 255, 255), backgroundColor=(128, 128, 128), failColor=(255, 0, 0), passColor=(0, 255, 0)):
		self.font = basefont
		self.pos = pos

		self.textColor = textColor
		self.failColor = failColor
		self.passColor = passColor
		self.backgroundColor = backgroundColor

		self.size = size

	def Render(self, surf, health, maxHealth, time):
		barSize = (self.size[0] * (health / maxHealth), self.size[1])

		barBgRect = pygame.Rect(self.pos, self.size)

		if health <= maxHealth / 5:
			color = self.failColor
		else:
			color = self.passColor

		pygame.draw.rect(surf, self.backgroundColor, (self.pos, self.size))
		if health > maxHealth:
			pygame.draw.rect(surf, color, (self.pos, barBgRect.size))
		else:
			pygame.draw.rect(surf, color, (self.pos, barSize))

		rText = self.font.render('Time: {0:.2f}s'.format(time), True, self.textColor)

		surf.blit(rText, (barBgRect.x + 1, barBgRect.centery - rText.get_height() / 2))
	
	@property
	def blitsRequired(self):
		return 1