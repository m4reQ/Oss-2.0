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

def GenSound(soundPath):
	"""
	loads music file to pygame sound object
	rtype: string
	returns: pygame.Sound
	"""

	sound = pygame.mixer.Sound(soundPath)

	return sound

class SoundContainer(object):
	containerID = 0

	def __init__(self, id=None, name=''):
		if not id:
			self.ID = SoundContainer.containerID
		else:
			self.ID = id
		self.name = name
		self.__sounds = {}

		SoundContainer.containerID += 1
		if debugging:
			print('[INFO]<', str(__name__), "> Sound container: '", str(self.name), "' initialized.")

	def AddSound(self, sound, soundName):
		if not type(sound).__name__ == 'Sound':
			raise Exception('[ERROR] Cannot add object of type ' + str(type(sound).__name__) + '. TextureContainer can only contain pygame.Surface type objects.')

		self.__sounds[soundName] = sound

	def GetSound(self, soundName):
		try:
			return self.__sounds[soundName]
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')

	def Dispose(self,soundName):
		try:
			del self.__sounds[soundName]
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')

	def DisposeAll(self):
		self.__sounds = {}

	def Rename(self, srcName, destName):
		#make copy of element
		item = self.__sounds[srcName]
		
		try:
			del self.__sounds[srcName]
			self.__sounds[destName] = item
		except KeyError:
			raise Exception('[ERROR] Dictionary key not found.')

	@property
	def sounds(self):
		return self.__sounds

	@property
	def is_empty(self):
		"""
		returns True if container is empty
		returns: bool
		"""
		return self.__sounds == {}
