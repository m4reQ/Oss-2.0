import os
import sys
import launcher

if __name__ == '__main__':
	launcher.Start(False)
else:
	raise Exception('[ERROR] Tried to access main launch method from external module.')

os.system('pause >NUL')
sys.exit()
