if __name__ == "__main__":
    import sys
    sys.exit()

import math

def GetPlayfield(width, height, CS):
	return {
		'topLeft': (width / 10 + CS, height / 10 + CS),
		'topRight': (width - width / 10 - CS, height / 10 + CS),
		'bottomLeft': (width / 10 + CS, height - height / 10 - CS),
		'bottomRight': (width - width / 10 - CS, height - height / 10 - CS),
		'minX': int(width / 10 + CS),
		'minY': int(height / 10 + CS),
		'maxX': int(width - width / 10 - CS),
		'maxY': int(height - height / 10 - CS),
		'width': int((width - width / 10 - CS) - (width / 10 + CS)),
		'height': int((height - height / 10 - CS) - (height / 10 + CS))}

def GetMaxPoints(maxCombo):
	points = 0
	for i in range(maxCombo):
		points += Stats.CalculatePoints(i, 10, 10, 10)

	return points

class Stats:
	@staticmethod
	def GetCS(CS):
		"""
		Calculates circle size.
		:param CS: (float) circle size
		:returns: int
		"""
		cs = int((109 - 9 * CS))

		return cs

	@staticmethod
	def GetAR(AR):
		"""
		Calculates circle approach speed
		:param AR: (float) circle approach time
		:returns: int
		"""
		ar = int(2000/(AR/2.75))
		return ar

	@staticmethod
	def GetHP(HP):
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
		return int(Stats.GetScoredPoints(combo) * Stats.GetARMultiplier(ar) * Stats.GetCSMultiplier(cs) * Stats.GetHPMultiplier(hp))

	@staticmethod
	def Clamp(value):
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