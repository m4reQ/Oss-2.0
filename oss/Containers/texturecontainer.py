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

def GenTexture(texPath, scale=None):
	"""
	loads texture to pygame image object
	rtype: string, int tuple
	returns: pygame.Image
	"""
	texture = pygame.image.load(texPath)

	if scale:
		texture = pygame.transform.scale(texture, scale)
	else:
		if debugging:
			print('[WARNING] Cannot scale texture because scaling is not enabled.')
	return texture

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
			print('[INFO]<', str(__name__), "> Texture container: '", str(self.name), "' initialized.")

	def AddTexture(self, texture, texName):
		if not type(texture).__name__ == 'Surface':
			raise Exception('[ERROR] Cannot add object of type ' + str(type(texture).__name__) + '. TextureContainer can only contain pygame.Surface type objects.')
		
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

	@property
	def textures(self):
		return self.__textures

	@property
	def is_empty(self):
		"""
		returns True if container is empty
		returns: bool
		"""
		return self.__textures == {}

	@property
	def count(self):
		return len(self.__textures)
