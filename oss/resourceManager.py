if __name__ == "__main__":
	import sys
	sys.exit()

import sys
import pygame
try:
	from PIL import Image
except ImportError:
	try:
		import Image
	except ImportError:
		print("Cannot load resource manager.")
		raise

class ResourceManager(object):
	def __init__(self, name, _id):
		self.name = name
		self.id = _id

		self._textures = {}
		self._sounds = {}
		self._fonts = {}

		self._mainFont = None

	def AddTexture(self, name, texture):
		self._textures[name] = texture

	def AddSound(self, name, sound):
		self._sounds[name] = sound

	def AddFont(self, name, font):
		self._fonts[name] = font

	def GetFont(self, name):
		return self._fonts[name]

	def AddMainFont(self, font):
		self._mainFont = font

	def GetTexture(self, name):
		return self._textures[name]

	def GetSound(self, name):
		return self._sounds[name]

	@property
	def Textures(self):
		return self._textures

	@property
	def Sounds(self):
		return self._sounds

	@property
	def Fonts(self):
		return self._fonts

	@property
	def MainFont(self):
		return self._mainFont

	@property
	def Count(self):
		return len(self._sounds) + len(self._textures) + len(self._fonts) + (1 if self._mainFont else 0)

	@property
	def Size(self):
		varSize = sum([sys.getsizeof(x) for x in self._sounds]) + sum([sys.getsizeof(x) for x in self._textures]) + sum([sys.getsizeof(x) for x in self._fonts]) + sys.getsizeof(self._mainFont)

		imgSize = 0
		for img in self.Textures.values():
			imgFile = Image.open(img.filename)
			imgSize += len(imgFile.fp.read())
			imgFile.close()
		
		soundSize = 0
		for sound in self.Sounds.values():
			soundFile = pygame.mixer.Sound(sound.filename).get_raw()
			soundSize += len(soundFile) * 2

		return varSize + imgSize + soundSize