import os
import random
import ctypes
from PIL import Image
import pygame
import math
import gc

user32 = ctypes.windll.user32

#-----Graphic utils-----
def ConvertImage(filename):
	"""
	converts image from jpg to png
	and adds alpha.
	rtype: str
	returns: None
	"""
	img = Image.open(filename)

	newImg = img.copy()
	newImg.putalpha(255)

	newImg.save(filename[:-4] + '.png')

def DimImage(image, dimPercent):
	"""
	Dims image and returns its copy.
	rtype: pygame.Surface, float
	returns: pygame.Surface
	"""
	img_d = image.copy()

	dark = pygame.Surface(img_d.get_size()).convert_alpha()
	dark.fill((0, 0, 0, dimPercent*255))
	img_d.blit(dark, (0, 0))

	return img_d

def translateCoord(data, res, mode):
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
		generates random color
		rtype: none
		returns: tuple
		"""
		return (random.randint(0,225), random.randint(0,225), random.randint(0,225))

class resolutions():
	SD = (640, 480)
	HD = (1360, 768)
	FHD = (1920, 1080)
	#4K = (3840, 2160) for now doesn't work

	@staticmethod
	def native():
		return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

	@staticmethod
	def user(width=0, height=0):
		return (width, height)

#-----Game utils-----
class stats:
	@staticmethod
	def getCS(CS):
		"""
		calculates circle size
		rtype: float
		returns: int
		"""
		cs = int((109 - 9 * CS))

		return cs

	@staticmethod
	def getAR(AR):
		"""
		calculates circle approach speed
		rtype: float
		returns: int
		"""
		ar = int(2000/(AR/2.75))
		return ar

	@staticmethod
	def getHP(HP):
		"""
		calculates hp units
		rtype: float
		returns: float
		"""
		hp = (HP+5) * 0.014
		return hp

	@staticmethod
	def getScoredPoints(combo):
		points = int(((combo-1) / 300) * 2 * combo + math.sqrt(2 * combo))
		return points

	@staticmethod
	def clamp(value):
		if value < 0:
			return 0
		if value > 10:
			return 10
		else:
			return value

#-----Function utils-----
def run_once(f):
	"""
	allows function to run only once in a loop
	can be used as a decorator
	rtype: function
	returns: function call or None
	"""
	def wrapper(*args, **kwargs):
		if not wrapper.has_run:
			wrapper.has_run = True
			return  f(*args, **kwargs)
	wrapper.has_run = False
	return wrapper

def run_interval(interval):
	"""
	runs function once per given loop
	executions
	can be used as a decorator
	rtype: function
	returns: function call or None
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
	indicates that the method is deprecated
	by a new one
	can be used as a decorator
	rtype: function, string
	returns: function call
	"""
	def decorator(f):
		def wrapper(*args, **kwargs):
			print('[WARNING] Method {} is deprecated and will be removed soon. Instead use: {}.'.format(f.__name__, newMethod))
			return f(*args, **kwargs)
		return wrapper
	return decorator

#-----Memory utils-----
def FreeMem(useDebugging):
	"""
	Triggers garbage collection
	rtype: bool
	returns: None
	"""

	objectsCount = gc.get_count()[0]

	if useDebugging:
		print('[INFO]<{}> Starting garbage collection.'.format(__name__))
	
	gc.collect()

	if useDebugging:
		print('[INFO]<{}> Freed {} objects.'.format(__name__, objectsCount - gc.get_count()[0]))

	
if __name__ == "__main__":
    pygame.quit()
    quit()