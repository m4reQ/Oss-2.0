import os
import sys
import launcher

if __name__ == '__main__':
	try:
		launcher.Start(False)
	except Exception as e:
		print("Error: {}".format(e))
		raise

else:
	raise RuntimeError('Error. Tried to access main launch method from external module.')

os.system('pause >NUL')
sys.exit()
