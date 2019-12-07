import pygame
import os

class Settings():
	def __init__(self):
		self.defaultset = False

	def LoadSetting(self, string):
		if string[0] == '#' or string == '' or string == '\n':
			pass
		elif string[0] != '/':
			key = str(string.partition("=")[0])
			value = str(string.partition("=")[2])
			value = value.split('\n')[0]

			key = key.replace(' ', '')
			value = value.replace(' ', '')

			if value.lower() == 'true':
				value = True
			elif value.lower() == 'false':
				value = False
			else:
				raise Exception('[ERROR] Error appeared during loading setting ' + key + '. Wrong value type ' + value + '.')

			return key, value

		if not self.defaultset:
			if string[0] == '/':
				setting = str(string.partition("=")[0])
				value = str(string.partition("=")[2])
				value = value.split('\n')[0]

				setting = setting.replace(' ', '')
				setting = setting.replace('/', '')
				value = value.replace(' ', '')
				
				os.environ[setting] = value

	def LoadFromFile(self, filepath):
		with open(filepath, mode='r') as f:
			for line in f.readlines():
				setting = self.LoadSetting(str(line))

				if setting:
					setattr(self, setting[0], setting[1])

	def LoadFromString(self, string):
		for line in string.splitlines():
			setting = self.LoadSetting(str(line))

			if setting:
				setattr(self, setting[0], setting[1])

	def ExportToFile(self, filename):
		raise Exception('[ERROR] Method is not implemented yet.')

	def GetSettings(self):
		return self.__dict__

	def GetSetting(self, setName):
		if not setName in self.__dict__.keys():
			raise Exception('[ERROR] Attribute ' + setName + " doesn't exist.")
		else:
			return getattr(self, setName)

if __name__ == '__main__':
	pygame.quit()
	quit()