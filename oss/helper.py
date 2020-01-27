import os
import traceback
import pygame

def logError(exception, file="log.txt"):
	"""
	Logs exception to specified log file.
	:param exception: (str) exception string
	:param file: (str) name of the log file
	"""
	with open(file, 'w+') as logf:
		logf.write(traceback.format_exc())

def exitAll():
	"""
	Hard exits the whole program with an additional pause.
	"""
	try:
		pygame.mixer.quit()
		pygame.quit()
		os.system("pause >NUL")
		quit()
	except Exception:
		pass

def ask(question):
	"""
	Creates a (Y/N) question with given question string.
	:param question: (str) question string
	:returns: bool
	"""
	q = ''
	while not any([q.upper() == 'Y', q.upper() == 'N']):
		try: q = raw_input(question + '(Y/N): ')
		except NameError: q = input(question + '(Y/N): ')
            
		if q.upper() == 'Y':
			return True
		elif q.upper() == 'N':
			return False

if __name__ == '__main__':
	exitAll()