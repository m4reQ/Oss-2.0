if __name__ == "__main__":
    import sys
    sys.exit()

from utils import resolutions
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
            self.cursorSize = prefDict["cursorSize"]
            self.lockMouse = prefDict["lockMouse"]
            self.masterVolume = prefDict["masterVolume"]
            self.darkenPercent = prefDict["darkenPercent"]
            self.resolution = tuple(prefDict["resolution"])
            self.fullscreen = prefDict["fullscreen"]
            self.borderless = prefDict["borderless"]
            self.keyBinds = prefDict["keyBinds"]
            self.mouseVisible = prefDict["mouseVisible"]
            self.autoGenerate = prefDict["autoGenerate"]
            self.useFpsCap = prefDict["useFpsCap"]
            self.interfaceEnabled = prefDict["interfaceEnabled"]
        else:
            self.cursorSize = 1.0
            self.lockMouse = False
            self.masterVolume = 0.75
            self.darkenPercent = 0.75
            self.resolution = resolutions.SD
            self.fullscreen = False
            self.borderless = True
            self.mouseVisible = False
            self.autoGenerate = True
            self.useFpsCap = False
            self.interfaceEnabled = True
            self.keyBinds = {
	            "kl": pygame.K_z,
	            "kr": pygame.K_x,
	            "debugUpdateWindow": pygame.K_BACKQUOTE,
	            "hideInterface": pygame.K_F10,
	            "debugGetPos": pygame.K_F1,
                "savePreferencies": pygame.K_s}
    
    def ExportToFile(self, filename):
        with open(filename, 'w+') as f:
            string = json.dumps(self.__dict__, sort_keys=True, indent=4)
            f.write(string)