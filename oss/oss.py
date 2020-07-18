import os
import sys

if __name__ == '__main__':
	try:
		import launcher
		launcher.Start(True)
	except Exception as e:
		print("Error: {}".format(e))
		raise

else:
	raise RuntimeError('Error. Tried to access main launch method from external module.')

os.system('pause >NUL')
sys.exit()
