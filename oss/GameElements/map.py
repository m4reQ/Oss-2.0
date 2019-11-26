import pygame
import GameElements.circle
from helper import Translate
from game import maps_path

is_loaded = False

def Load_map(file):
	"""
	rtype: string
	returns: array
	"""
	global is_loaded

	if is_loaded:
		raise Exception('[ERROR] Map is already loaded.')
	
	with open(maps_path + file + '.txt', "r") as f:
		if not f.mode == 'r':
			raise Exception("[ERROR] File doesn't have assigned required usage mode.")
		
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

def Make_map(data, targetRes):
	"""
	rtype: array, tuple
	returns: array
	"""
	lenght = len(data)
	ptr = 0

	circles = []
	for element in data:
		while ptr <= lenght-1:
			try:
				posX = float(data[ptr])
				posY = float(data[ptr+1])
				time = int(data[ptr+2])

				ptr += 3

				tposX, tposY = Translate((posX, posY), targetRes, 1)

				obj = circle.Circle(int(tposX), int(tposY), time)
				circles.append(obj)
			except IndexError:
				raise Exception('[ERROR] Cannot make object' + str(obj) + '. \nCannot load map. Maybe map has outdated or invalid format.')

	return circles

if __name__ == '__main__':
	pygame.quit()
	quit()