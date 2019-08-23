import pygame
import circle

class Map():
	is_loaded = False
	
	def __init__(self, mode):
		global DEBUG_MODE
		DEBUG_MODE = mode

	def Load_map(self, file):
		"""
		rtype: string
		returns: array
		"""
		global DEBUG_MODE

		if Map.is_loaded:
			DEBUG_EXCEPTION = "Map is already loaded."

			return DEBUG_EXCEPTION
		
		f = open('maps/' + file + '.txt', "r")
		if not f.mode == 'r':
			if DEBUG_MODE:
				DEBUG_EXCEPTION = "File doesn't have assigned required usage mode."

			return DEBUG_EXCEPTION
			
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

		if DEBUG_MODE:
			print("Raw circle data sheet: " + str(formatted_data))

		return formatted_data
