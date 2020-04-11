import os
import launcher

if __name__ == '__main__':
	launcher.Start()
else:
	raise Exception('[ERROR] Tried to access main launch method from external module.')

os.system('pause >NUL')
quit()
