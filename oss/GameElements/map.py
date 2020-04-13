if __name__ == '__main__':
	quit()

from Utils.graphics import TranslateCoord, TranslationMode
from Utils.game import GetMaxPoints
from launcher import debugging

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

				if line[0] == '#' or line[0] == "[":
					continue

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

	except IOError:
		print("Error cannot load map: File {} didn't found.".format(filepath))
		return -1 #indicate that a error appeared

	return data

def MakeMap(filepath, targetRes):
	"""
	rtype: array, tuple
	returns: array
	"""
	data = ParseMap(filepath)

	if data == -1:
		return

	#import circles here to avoid circular import
	from .circle import Circle

	circles = []
	for element in data:
		try:
			posX = float(element[0])
			posY = float(element[1])
			time = int(element[2])

			tposX, tposY = TranslateCoord((posX, posY), targetRes, TranslationMode.Decode)

			obj = Circle((tposX, tposY), time)
			circles.append(obj)
		except IndexError:
			print('Cannot make object {}.\n Maybe map has outdated or invalid format.'.format(str(obj)))
			return
	
	if debugging:
		print('[INFO]<{}> Map "{}" loaded.'.format(__name__, filepath))

	return circles

class Map:
	resolution = (0, 0)

	@staticmethod
	def ReadHeader(filename):
		try:
			with open(filename) as f:
				while True:
					first = f.readline()
					first = first.replace("\n", "")
					if first[0] == "#":
						continue
					if first[0] == "[" and first[-1] == "]":
						break
		except IOError:
			print("Cannot load map: File {} didn't found.".format(filename))
			return (0, 0, 0, -1)

		first = first[1:-1]
		data = first.split(",")
		data = [x.replace(" ", "") for x in data]
		data[-1] = data[-1].replace("\n", "")

		return (data[0], int(data[1]), int(data[2]), 1)

	def __init__(self, filename):
		self.filename = filename
		self.name, self.id, self.length, self.loadSuccess = Map.ReadHeader(filename)

		if self.loadSuccess == -1:
			print("Cannot load map from '{}'.".format(filename))

		self.objects = MakeMap(filename, Map.resolution)
		self.objectsLeft = self.objects[:]
		self.objCount = len(self.objects)

		self.shouldPlay = True

		self.maxCombo = self.objCount
		self.maxPoints = GetMaxPoints(self.maxCombo)

	def __str__(self):
		return "Map - Name: {}, ID: {}, Length: {}, Objects: {}".format(self.name, self.id, self.length, self.objCount)

class EmptyMap(object):
	def __init__(self):
		self.objectsLeft = []
		self.shouldPlay = True

		self.loadSuccess = 1
		self.length = float('inf')
	