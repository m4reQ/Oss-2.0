import os
import traceback
import pygame

def logError(exception):
	with open('log.txt', 'w+') as logf:
		logf.write(traceback.format_exc())

def exitAll():
	try:
		pygame.mixer.quit()
		pygame.quit()
		os.system("pause >NUL")
		quit()
	except Exception:
		pass

def ask(question):
	"""
	creates a (Y/N) question with given question string
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

if __name__ == '__main__':
	exitAll()