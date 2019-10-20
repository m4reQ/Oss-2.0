import pygame
import circle

is_loaded = False

def Load_map(file):
	"""
	rtype: string
	returns: array
	"""
	global is_loaded
	if is_loaded:
		raise Exception('Map is already loaded.')
	
	with open('maps/' + file + '.txt', "r") as f:
		if not f.mode == 'r':
			raise Exception("File doesn't have assigned required usage mode.")
		
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

	formatted_data = []
	for element in data:
		new_element = element.split('\n')
		e = new_element[0]
		formatted_data.append(e)

	is_loaded =True

	return formatted_data

def Make_map(data):
	"""
	rtype: array
	returns: array
	"""
	lenght = len(data)
	ptr = 0

	circles = []
	for element in data:
		while ptr <= lenght-1:
			try:
				posX = int(data[ptr])
				posY = int(data[ptr+1])
				time = int(data[ptr+2])

				ptr += 3

				obj = circle.Circle(posX, posY, time)
				circles.append(obj)
			except IndexError:
				raise Exception('Program stopped incorrectly. Cannot make object, invalid map format. \nCannot load map. Maybe map has outdated or invalid format.')

	return circles
