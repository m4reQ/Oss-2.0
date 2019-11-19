import math
import random
import ctypes
import os

user32 = ctypes.windll.user32

def LoadSettings(filepath):
	"""
	loads settings from specified file
	rtype: string
	returns:list
	"""
	values = []
	with open(filepath, mode='r') as f:
		for line in f.readlines():
			if str(line)[0] == '#' or str(line) == '' or str(line) == '\n':
				pass
			else:
				key = str(line.partition("=")[0])
				value = str(line.partition("=")[2])
				value = value.split('\n')[0]

				key = key.replace(' ', '')
				value = value.replace(' ', '')

				if value.lower() == 'true':
					value = True
				elif value.lower() == 'false':
					value = False
				else:
					raise Exception('[ERROR] Error appeared during settings loading. Wrong value type.')

				values.append(value)

	return values

def SetDisplaySettings(sdl_driver, sdl_windowpos):
	os.environ['SDL_VIDEODRIVER'] = sdl_driver
	os.environ['SDL_VIDEO_WINDOW_POS'] = sdl_windowpos

def ask(question):
	"""
	creates a (Y/N) question with given question string
	rtype:string
	returns: bool
	"""
	q = ''
	while not any([q.upper() == 'Y', q.upper() == 'N']):
		try: q = raw_input(question + '(Y/N): ')
		except NameError: q = input(question + '(Y/N): ')
            
		if q.upper() == 'Y':
			return True
		elif q.upper() == 'N':
			return False

def Translate(data, res, mode):
	"""
	translates position of point to unified coordinate system
	max value in each direction is 1.0 and the min is 0.0
	available modes are: 0-encode, 1-decode
	rtype: tuple, tuple, int
	returns: tuple
	"""

	x, y = data
	resX, resY = res

	#encode
	if mode == 0:
		uX = x / resX
		uY = y / resY

		return (uX, uY)
	#decode
	elif mode == 1:
		tX = x * resX
		tY = y * resY

		return (int(tX), int(tY))
	else:
		raise Exception('[ERROR] Invalid translation mode.')

class color:
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	yellow = (128,128,0)
	purple = (128,0,128)
	cyan = (0,128,128)
	white = (255,255,255)
	black = (0,0,0)
	gray = (128, 128, 128)

	def random():
		"""
		generates random color
		rtype: none
		returns: tuple
		"""
		color = (random.randint(0,225), random.randint(0,225), random.randint(0,225))
		return color

class Resolutions:
	SD = (640, 480)
	HD = (1360, 768)
	FHD = (1920, 1080)
	#4K = (3840, 2160) for now doesn't work
	native = (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

	def user(width=0, height=0):
		return (width, height)

class stats:
	def getCS(CS):
		"""
		calculates circle size
		rtype: float
		returns: int
		"""
		if CS > 5:
			cs = int(round(150/(math.sqrt(CS)*2)))
		else:
			cs = int(round(150/(math.sqrt(CS)*2.5)))
		return cs

	def getAR(AR):
		"""
		calculates circle approach speed
		rtype: float
		returns: int
		"""
		ar = int(2000/(AR/3))
		return ar

	def getHP(HP):
		"""
		calculates hp units
		rtype: float
		returns: float
		"""
		hp = (HP+5) * 0.01
		return hp