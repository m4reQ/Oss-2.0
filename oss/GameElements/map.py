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

def ParseMap(filepath):
	data = []
	lineCount = 0

	try:
		with open(filepath, "r") as f:
			for line in f.readlines():
				lineCount += 1

				if str(line) == '#':
					break
				else:
					line = str(line)
					lineData = line.split(",")

					newLineData = []
					for x in lineData:
						x = x.replace("\n", "")
						x = x.replace(" ", "")

						try:
							x = float(x)
						except ValueError: #if even a single fragment of any line failed to parse stop loading rest of map
							if debugging:
								print("[ERROR]<{}> Invalid map format at line {}".format(__name__, lineCount))

							return -1

						newLineData.append(x)
						
					data.append(newLineData)

	except FileNotFoundError:
		print("Error cannot load map: File {} didn't found.".format(filepath))
		return -1 #indicate that a error appeared

	return data

def Make_map(filepath, targetRes):
	"""
	rtype: array, tuple
	returns: array
	"""
	global is_loaded

	data = ParseMap(filepath)

	if data == -1:
		print("Cannot load map from '{}'.".format(filepath))
		return -1

	#import circles here to avoid cyclic import
	from .circle import Circle

	circles = []
	for element in data:
		try:
			posX = float(element[0])
			posY = float(element[1])
			time = int(element[2])

			tposX, tposY = translateCoord((posX, posY), targetRes, 1)

			obj = Circle(int(tposX), int(tposY), time)
			circles.append(obj)
		except IndexError:
			print('[ERROR] Cannot make object {}.\n Maybe map has outdated or invalid format.'.format(str(obj)))
			return
	
	if debugging:
		print('[INFO]<{}> Map "{}" loaded.'.format(__name__, filepath))

	is_loaded = True

	return circles

if __name__ == '__main__':
	exitAll()