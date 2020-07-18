if __name__ == "__main__":
	import sys
	sys.exit()

from Utils.other import GetFileExtension, GetFilenameFromPath
from Utils.debug import Log, LogLevel
import pygame

LOG_TEXTURES = False

class TextureType:
	PNG, JPG = range(2)

class Texture(object):
	texId = 0

	def __init__(self, filename):
		self.filename = filename

		self.id = Texture.texId
		Texture.texId += 1

		extension = GetFileExtension(GetFilenameFromPath(filename))
		if extension == "jpg" or extension == "jpeg":
			fileType = TextureType.JPG
		elif extension == "png":
			fileType = TextureType.PNG
		else:
			raise RuntimeError("Invalid file extension: {}".format(extension))

		self.tex = self.LoadTexture(filename, fileType)

		self._width = self.tex.get_width()
		self._height = self.tex.get_height()

	def LoadTexture(self, filename, type):
		try:
			if type == TextureType.JPG:
				tex = pygame.image.load(filename).convert()
			elif type == TextureType.PNG:
				tex = pygame.image.load(filename).convert_alpha()
			else:
				raise RuntimeError("Invalid texture type.")
		except Exception:
			Log("Cannot load texture from file '{}'.".format(filename), LogLevel.Error, __name__)
			raise

		return tex

	def Scale(self, scale):
		self.ScaleXY(scale, scale)
	
	def ScaleXY(self, x, y):
		self.tex = pygame.transform.scale(self.tex, (x, y))
		self._width = x
		self._height = y
	
	def ScaleLinear(self, scale):
		self.ScaleLinearXY(scale, scale)
		
	def ScaleLinearXY(self, x, y):
		self.tex = pygame.transform.smoothscale(self.tex, (x, y))
		self._width = x
		self._height = y

	def Dim(self, dimPercent):
		dark = pygame.Surface((self.Width, self.Height)).convert_alpha()
		dark.fill((0, 0, 0, int(dimPercent * 255)))

		self.tex.blit(dark, (0, 0))
	
	def SetAlpha(self, alpha):
		self.tex.set_alpha(alpha)

	def Color(self, r, g, b):
		self.tex.fill((r, g, b, 0), None, pygame.BLEND_RGBA_ADD)

	def Get(self):
		return self.tex

	@property
	def Width(self):
		return self._width

	@property
	def Height(self):
		return self._width