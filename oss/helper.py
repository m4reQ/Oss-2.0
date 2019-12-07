import math
import random
import ctypes
import os
import traceback

user32 = ctypes.windll.user32

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
			print('[WARNING] Method ' + f.__name__ + ' is deprecated and will be removed soon. Instead use: ' + newMethod)
			return f(*args, **kwargs)
		return wrapper
	return decorator

def logError(exception):
	if not str(exception)[:6] == '[INFO]':
		with open('log.txt', 'w+') as logf:
			logf.write(traceback.format_exc())

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

class color(object):
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
		return (random.randint(0,225), random.randint(0,225), random.randint(0,225))

class Resolutions(object):
	SD = (640, 480)
	HD = (1360, 768)
	FHD = (1920, 1080)
	#4K = (3840, 2160) for now doesn't work

	def native():
		return (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))

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
		hp = (HP+5) * 0.014
		return hp

if __name__ == '__main__':
	pygame.quit()
	quit()