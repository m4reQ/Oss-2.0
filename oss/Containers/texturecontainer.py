import pygame

debugging = False

def SetDebugging(val):
	"""
	Sets debugging mode to given value.
	:param val: (bool) value to set debugging
	"""
	global debugging
	debugging = val

def GenTexture(texPath):
	"""
	Creates texture from given image.
	:param texPath: (string) actual texture file path
	:returns: pygame.Surface
	"""
	return pygame.image.load(texPath)

class TextureContainer(object):
	containerID = 0
	
	def __init__(self, id=None, name=''):
		if not id:
			self.ID = TextureContainer.containerID
		else:
			self.ID = id
		self.name = name
		self.__textures = {}

		TextureContainer.containerID += 1
		if debugging:
			print('[INFO]<{}> Texture container: "{}" initialized.'.format(__name__, self.name))

	def AddTexture(self, texture, texName):
		if not type(texture).__name__ == 'Surface':
			raise Exception('[ERROR] Cannot add object of type {}. TextureContainer can only contain pygame.Surface type objects.'.format(type(texture).__name__))
		
		self.__textures[texName] = texture

	def GetTexture(self, texName):
		try:
			return self.__textures[texName]
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')

	def Dispose(self,texName):
		try:
			del self.__textures[texName]
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')

	def DisposeAll(self):
		self.__textures = {}

	def Rename(self, srcName, destName):
		#make copy of element
		item = self.__textures[srcName]
		
		try:
			del self.__textures[srcName]
			self.__textures[destName] = item
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')
	
	def ScaleTexture(self, texName, scale):
		self.__textures[texName] = pygame.transform.scale(self.__textures[texName], (scale, scale))
	
	def ScaleTextureXY(self, texName, scaleX, scaleY):
		self.__textures[texName] = pygame.transform.scale(self.__textures[texName], (scaleX, scaleY))

	@property
	def textures(self):
		return self.__textures

	@property
	def is_empty(self):
		"""
		Returns True if container is empty
		:returns: bool
		"""
		return self.__textures == {}

	@property
	def count(self):
		return len(self.__textures)

if __name__ == '__main__':
	quit()
	pygame.quit()