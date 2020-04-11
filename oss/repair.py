if __name__ == '__main__':
	quit()

def CheckResponse():
	return True

import os

def InstallPackages():
	try:
		os.system('py -m pip install -r requirements.txt')
	except Exception:
		try:
			os.system('python -m pip install -r requirements.txt')
		except Exception:
			print('Cannot install packages.')
			raise
	
	print('Modules installed. Please restart application.')
	os.system("pause >NUL")
	quit()