if __name__ == "__main__":
	import sys
	sys.exit()

from Utils.graphics import Resolutions
import pygame
import json

class Preferencies:
	PREFS_FILE = "defaultPrefs.json"

	@classmethod
	def ImportFromFile(cls, filename):
		string = open(filename, 'r').read()
		return cls(json.loads(string))

	def __init__(self, prefDict={}):
		if not len(prefDict) == 0:
			for pref in prefDict.keys():
				setattr(self, pref, prefDict[pref])
		else:
			self.cursorSize = 1.0
			self.lockMouse = False
			self.masterVolume = 0.75
			self.darkenPercent = 0.75
			self.useNewFpsCounter = True
			self.resolution = Resolutions.SD
			self.fullscreen = False
			self.borderless = True
			self.mouseVisible = False
			self.autoGenerate = True
			self.useFpsCap = False
			self.interfaceEnabled = True
			self.mouseButtonsDisable = False
			self.keyBinds = {
				"kl": pygame.K_z,
				"kr": pygame.K_x,
				"hideInterface": pygame.K_F10,
				"savePreferencies": pygame.K_s,
				"debugUpdateWindow": pygame.K_BACKQUOTE,
				"debugProfile": pygame.K_BACKSLASH,
				"debugGetPos": pygame.K_F1}
	
	def ExportToFile(self, filename):
		with open(filename, 'w+') as f:
			string = json.dumps(self.__dict__, sort_keys=True, indent=4)
			f.write(string)