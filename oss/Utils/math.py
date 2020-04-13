if __name__ == "__main__":
    import sys
    sys.exit()

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