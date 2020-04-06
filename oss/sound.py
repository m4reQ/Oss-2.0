import pygame

LOG_SOUNDS = False

class Sound(object):
	soundId = 0

	def __init__(self, filename):
		self.filename = filename

		self.id = Sound.soundId
		Sound.soundId += 1

		self.sound = self.LoadSound(filename)

		if LOG_SOUNDS:
			print("[INFO]<{}> Sound from file '{}' initialized succesfully.".format(__name__, filename))

	def LoadSound(self, filename):
		try:
			sound = pygame.mixer.Sound(filename)
		except Exception as e:
			print("[ERROR]<{}> Error: {}. Cannot load sound from file: {}".format(__name__, e, filename))

		return sound

	def SetVolume(self, volume):
		self.sound.set_volume(volume)

	def Play(self):
		self.sound.play()