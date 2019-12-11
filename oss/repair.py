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
	if not (ver[0] >= 3) and not (ver[1] >= 0):
		print("You don't have required python version")
		print("Go to a python official website to download latest versions. https://www.python.org/downloads")
		os.system('pause >NUL')
		quit()
	else:
		try:
			os.system('py -m pip install -r requirements.txt')
		except Exception as e:
			print('Cannot install packages. ', e)
			exitAll()

		print('Modules installed.')
		exitAll()

if __name__ == '__main__':
	pygame.quit()
	quit()