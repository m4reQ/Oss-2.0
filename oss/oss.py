from helper import logError
import launcher

try:
	if __name__ == '__main__':
		launcher.Start()
	else:
		raise Exception('[ERROR] Tried to access main launch method from external module.')
except Exception as e:
	logError(e)
	print(e)
	quit()