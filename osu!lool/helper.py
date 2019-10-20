import math
import random
import ctypes

class color():
	def __init__(self):
		pass

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
		rtype: none
		returns: tuple
		"""
		color = (random.randint(0,225), random.randint(0,225), random.randint(0,225))
		return color

user32 = ctypes.windll.user32

resolutions = {
	'SD': (640, 480),
	'HD': (1360, 768),
	'FHD': (1920, 1080),
	'4K': (3840, 2160),
	'native': (user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))
}

def ask(question):
	"""
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

class stats():
	def __init__(self):
		pass

	def getCS(CS):
		"""
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
		rtype: float
		returns: int
		"""
		ar = int(2000/(AR/3))
		return ar

	def getHP(HP):
		"""
		rtype: float
		returns: float
		"""
		hp = (HP+5) * 0.01
		return hp