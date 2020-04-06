import pygame

LOG_TEXTURES = False

class Texture(object):
	texId = 0

	def __init__(self, filename):
		self.filename = filename

		self.id = Texture.texId
		Texture.texId += 1

		self.tex = self.LoadTexture(filename)

		self._width = self.tex.get_width()
		self._height = self.tex.get_height()

		if LOG_TEXTURES:
			print("[INFO]<{}> Texture from file '{}' initialized succesfully.".format(__name__, filename))

	def LoadTexture(self, filename):
		try:
			tex = pygame.image.load(filename).convert_alpha()
		except Exception as e:
			print("[ERROR]<{}> Error: {} Cannot load texture from file: {}".format(__name__, e, filename))

		return tex

	def Scale(self, scale):
		self.ScaleXY(scale, scale)

	def ScaleXY(self, x, y):
		self.tex = pygame.transform.scale(self.tex, (x, y))
		self._width = x
		self._height = y

	def Dim(self, dimPercent):
		dark = pygame.Surface((self.Width, self.Height)).convert_alpha()
		dark.fill((0, 0, 0, dimPercent*255))

		self.tex.blit(dark, (0, 0))

	def Get(self):
		return self.tex

	@property
	def Width(self):
		return self._width

	@property
	def Height(self):
		return self._width