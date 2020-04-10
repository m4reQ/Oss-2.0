if __name__ == "__main__":
    quit()

import os
import random
import ctypes
from PIL import Image
import pygame
import math
import gc

user32 = ctypes.windll.user32

#-----Math utils-----
def Clamp(val, min, max):
	"""
	Clamps a given value to be between max and min parameters.
	Converts value to float.
	:param val: (float, int) Value to clamp
	:param min: (float, int) Minimal value
	:param max: (float, int) Maximal value
	:returns: float
	"""
	val = float(val)
	min = float(min)
	max = float(max)

	if val < min:
		return min
	elif val > max:
		return max
	else:
		return val

def GetMax(val, maximum):
	"""
	Returns higher of the two given values.
	:param val: (float, int) Value to clamp
	:param max: (float, int) Maximal value
	:returns: float
	"""
	val = float(val)
	maximum = float(maximum)
	return max([val, maximum])

#-----Graphic utils-----
def ConvertImage(filepath):
	"""
	Converts image from jpg to png and adds alpha.
	Shouldn't be used frequently because of very low performance.
	:param filepath: (str) Path to an image
	"""
	img = Image.open(filepath)

	newImg = img.copy()
	newImg.putalpha(255)

	newImg.save(filepath[:-4] + '.png')

def DimImage(image, dimPercent):
	"""
	Dims image and returns its copy.
	:param image: (pygame.Surface) Image to dim
	:param dimPercent: (float) Indicates how dark an image should be
	:returns: pygame.Surface
	"""
	img_d = image.copy()

	dark = pygame.Surface(img_d.get_size()).convert_alpha()
	dark.fill((0, 0, 0, dimPercent*255))
	img_d.blit(dark, (0, 0))

	return img_d

def translateCoord(data, res, mode):
	"""
	Translates position of point to unified coordinate system
	Max value in each direction is 1.0 and the min is 0.0
	:param data: (tuple(float, float)) Position to be translated
	:param res: (tuple(float, float)) Target resolution
	:param mode: (int) Work mode. Available modes are: 0-encode, 1-decode
	:returns: (tuple(int, int), tuple(float, float))
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
		x = Clamp(x, 0, 1)
		y = Clamp(y, 0, 1)

		tX = x * resX
		tY = y * resY

		return (int(tX), int(tY))
	else:
		raise Exception('[ERROR] Invalid translation mode.')

def GetTextColor(bgColor):
	avg = sum(bgColor) / len(bgColor)
	textColor = (255, 255, 255) if avg <= 128 else (0, 0, 0)

	return textColor

def IsFullyVisible(rect, winSize):
	xTest = rect.left >= 0 and rect.right <= winSize[0]
	yTest = rect.bottom <= winSize[1] and rect.top >= 0

	return xTest and yTest

def IsPartiallyVisible(rect, winSize):
	xTest = rect.left >= 0 or rect.right <= winSize[0]
	yTest = rect.bottom <= winSize[1] or rect.top >= 0

	return (xTest or yTest) and not IsFullyVisible(rect, winSize)

class color():
	red = (255,0,0)
	green = (0,255,0)
	blue = (0,0,255)
	yellow = (128,128,0)
	purple = (128,0,128)
	cyan = (0,128,128)
	white = (255,255,255)
	black = (0,0,0)
	gray = (128, 128, 128)

	@staticmethod
	def random():
		"""
		Generates random color.
		:returns: tuple(int, int, int)
		"""
		return (random.randint(0,225), random.randint(0,225), random.randint(0,225))

	@staticmethod
	def GetNegative(color):
		r = 255 - color[0]
		g = 255 - color[1]
		b = 255 - color[2]

		return (r, g, b)

class resolutions():
	SD = (640, 480)
	HD = (1360, 768)
	FHD = (1920, 1080)

	@staticmethod
	def native():
		"""
		Uses the native display resolution.
		:returns: tuple(int, int)
		"""
		return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

	@staticmethod
	def user(width=0, height=0):
		return (width, height)

#-----Game utils-----
def GetMaxPoints(maxCombo):
	points = 0
	for i in range(maxCombo):
		points += stats.CalculatePoints(i, 10, 10, 10)

	return points

class stats:
	@staticmethod
	def getCS(CS):
		"""
		Calculates circle size.
		:param CS: (float) circle size
		:returns: int
		"""
		cs = int((109 - 9 * CS))

		return cs

	@staticmethod
	def getAR(AR):
		"""
		Calculates circle approach speed
		:param AR: (float) circle approach time
		:returns: int
		"""
		ar = int(2000/(AR/2.75))
		return ar

	@staticmethod
	def getHP(HP):
		"""
		Calculates hp units
		:param HP: (float) health drop rate
		:returns: float
		"""
		hp = (HP+5) * 0.014
		return hp
	
	@staticmethod
	def GetARMultiplier(AR):
		"""
		Calculates score multiplier based on given AR
		:param AR: (float) circle approach time
		:returns: float
		"""
		if AR > 0 and AR <= 7:
			return math.log(AR, 3) + 1
		elif AR > 7 and AR <= 9:
			return math.sqrt(AR ** 2 + 1) - 4.3
		elif AR > 9 and AR <= 10:
			return math.cos(AR) + AR - (AR / 2.7)
		else:
			return 0.0
	
	@staticmethod
	def GetCSMultiplier(CS):
		"""
		Calculates score multiplier based on given CS
		:param CS: (float) circle size
		:returns: float
		"""
		if CS > 0 and CS < 6:
			return (CS + 1) / 4
		elif CS >= 6 and CS <= 10:
			return CS - 4.25
		else:
			return 0.0
	
	@staticmethod
	def GetHPMultiplier(HP):
		"""
		Calculates score multiplier based on given HP
		:param HP: (float) hp drop
		:returns: float
		"""
		if HP > 0 and HP <= 10:
			return HP / 10.0
		else:
			return 0.0

	@staticmethod
	def GetScoredPoints(combo):
		"""
		Calculates points get for a hit at the given combo.
		:param combo: (int) actual combo
		:returns: int
		"""
		return int(((combo-1) / 300) * 2 * combo + math.sqrt(2 * combo))
	
	@staticmethod
	def CalculatePoints(combo, ar, cs, hp):
		"""
		Calculates points get for a hit a the given combo and multiplies it by all stat modifiers
		:param combo: (int) actual combo
		:param ar: (float) circle approach rate
		:param cs: (float) circle size
		:param hp: (float) hp drop
		:returns: int
		"""
		return int(stats.GetScoredPoints(combo) * stats.GetARMultiplier(ar) * stats.GetCSMultiplier(cs) * stats.GetHPMultiplier(hp))

	@staticmethod
	def clamp(value):
		"""
		Clamps statistic value to be 0-10.
		:param value: (float) stat to be clamped
		:returns: float
		"""
		if value < 0:
			return 0
		if value > 10:
			return 10
		else:
			return value

#-----Function utils-----
def run_once(f):
	"""
	Allows function to run only once in a loop. Can be used as a decorator.
	:param f: (function) function that has to be run
	:returns: (function call, None)
	"""
	def wrapper(*args, **kwargs):
		if not wrapper.has_run:
			wrapper.has_run = True
			return  f(*args, **kwargs)
	wrapper.has_run = False
	return wrapper

def run_interval(interval):
	"""
	Runs function once per given loop executions number. Can be used only as a decorator!
	:param interval: (int) indicates how many loops function has to sleep before call
	:returns: (function call, None)
	"""
	def decorator(f):
		def wrapper(*args, **kwargs):
			if wrapper.count == interval:
				wrapper.count = 0
				return f(*args, **kwargs)
			else:
				wrapper.count += 1
		wrapper.count = 0
		return wrapper
	return decorator

def deprecated(newMethod):
	"""
	Indicates that the method is deprecated by a new one. Can be used only as a decorator!
	:param newMethod: (str) name of the new function.
	:returns: (function call, None)
	"""
	def decorator(f):
		def wrapper(*args, **kwargs):
			print('[WARNING] Method {} is deprecated and will be removed soon. Instead use: {}.'.format(f.__name__, newMethod))
			return f(*args, **kwargs)
		return wrapper
	return decorator

#-----Memory utils-----
def FreeMem(useDebugging, msg='Starting garbage collection'):
	"""
	Triggers garbage collection.
	:param useDebugging: (bool) tells if function should indicate a call
	:param msg: (str) message to display before starting GC
	"""

	try:
		objectsCount = gc.get_count()[0]
		if useDebugging:
			print('[INFO]<{}> {}.'.format(__name__, msg))
		gc.collect()
		if useDebugging:
			print('[INFO]<{}> Freed {} objects.'.format(__name__, objectsCount - gc.get_count()[0]))
	except Exception as e:
		print('[ERROR]<{}> An error occured during garbage collection. \n{}'.format(__name__, str(e)))