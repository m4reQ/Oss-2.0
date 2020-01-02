import os
from helper import exitAll
debugging = False

def SetDebugging(val):
	"""
	sets debugging mode to given value
	rtype: bool
	returns: None
	"""
	global debugging
	debugging = val

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
				raise Exception('[ERROR] Error appeared during loading setting {}. Wrong value type {}.'.format(key, value))

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
		from datetime import datetime #for current time and date
		import getpass #for username

		now = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
		user = getpass.getuser()

		if debugging:
			print('[INFO]<{}> Exporting settings to "{}" file'.format(__name__, filename))

		with open(filename, 'a') as f:
			for setting, value in self.__dict__.items():
				string = '{} = {}\n'.format(setting, value)
				f.write(string)
			f.write('#Settings configuration for {} generated {}.'.format(user, now))

		if debugging:
			print('[INFO]<{}> Export done.'.format(__name__))

	def GetSettings(self):
		return self.__dict__

	def GetSetting(self, setName):
		if not setName in self.__dict__.keys():
			raise Exception("[ERROR] Attribute {} doesn't exist".format(setName))
		else:
			return getattr(self, setName)

if __name__ == '__main__':
	exitAll()