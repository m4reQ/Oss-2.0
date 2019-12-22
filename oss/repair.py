def Check_response():
	"""
	rtype: none
	returns: bool
	"""
	return True

import os
import sys
from helper import ask, exitAll

ver = sys.version_info

def main():
	if ver[0] >= 3:
		try: #try to use newest python's py launcher
			os.system('py -m pip install -r requirements.txt')
		except Exception as e: #if it's not there use the old method
			os.system('python -m pip install -r requirements.txt')
		finally: #if all methods fail then it's nothing to do with it
			print('Cannot install packages. {}'.format(e))
			exitAll()
	elif ver[0] < 3:
		try:
			os.system('python -m pip install -r requirements.txt')
		except Exception as e:
			print('Cannot install packages. {}'.format(e))
			exitAll()

	print('Modules installed. Please restart application.')
	os.system('pause >NUL')
	exitAll()

if __name__ == '__main__':
	pygame.quit()
	quit()