from helper import logError, exitAll
from utils import translateCoord

is_loaded = False

debugging = False

def SetDebugging(val):
	"""
	sets debugging mode to given value
	rtype: bool
	returns: None
	"""
	global debugging
	debugging = val

def Load_map(file):
	"""
	rtype: string
	returns: array
	"""
	global is_loaded

	#import paths here to avoid cyclic import
	from launcher import maps_path

	if is_loaded:
		raise Exception('[ERROR] Map is already loaded.')

	try:
		with open(maps_path + file + '.txt', "r") as f:
			data = []
			for line in f.readlines():
				if str(line) == '#':
					f.close()
					break
				else:
					data.append(line)

		try:
			for element in data:
				data.remove('\n')
		except ValueError:
			pass
	except Exception as e:
		logError(e)
		raise Exception('[ERROR] Cannot open file "{}".'.format(file))

	formatted_data = []
	for element in data:
		new_element = element.split('\n')
		e = new_element[0]
		formatted_data.append(e)

	if debugging:
		print('[INFO]<{}> Map "{}" loaded.'.format(__name__, file))

	is_loaded = True

	return formatted_data

def Make_map(data, targetRes):
	"""
	rtype: array, tuple
	returns: array
	"""
	ptr = 0

	#import circles here to avoid cyclic import
	from .circle import Circle

	circles = []
	for element in data:
		while ptr <= len(data)-1:
			try:
				posX = float(data[ptr])
				posY = float(data[ptr+1])
				time = int(data[ptr+2])

				ptr += 3

				tposX, tposY = translateCoord((posX, posY), targetRes, 1)

				obj = Circle(int(tposX), int(tposY), time)
				circles.append(obj)
			except IndexError:
				raise Exception('[ERROR] Cannot make object {}.\nCannot load map. Maybe map has outdated or invalid format.'.format(str(obj)))

	return circles

if __name__ == '__main__':
	exitAll()