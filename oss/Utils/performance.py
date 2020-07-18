if __name__ == "__main__":
    import sys
    sys.exit()

import gc

try:
	from time import perf_counter as timer
except (ImportError, ModuleNotFoundError):
	from time import time as timer

from time import sleep

from Utils.debug import Log, LogLevel

__GCTHREAD_STOP_FLAG = False

def FreeMem(msg='Starting garbage collection'):
	"""
	Triggers garbage collection.
	:param useDebugging: (bool) tells if function should indicate a call
	:param msg: (str) message to display before starting GC
	"""

	try:
		objectsCount = gc.get_count()[0]
		Log(msg, LogLevel.Info, __name__)
		gc.collect()
		Log("Freed {} objects.".format(objectsCount - gc.get_count()[0]), LogLevel.Info, __name__)
	except Exception as e:
		Log("An error occured during garbage collection: {}".format(str(e)), LogLevel.Error, __name__)

def TimedGarbageCollect(interval):
	while True:
		objectsCount = gc.get_count()[0]
		gc.collect()
		Log("GC thread freed {} objects.".format(objectsCount - gc.get_count()[0]), LogLevel.Info, __name__)
		sleep(interval)
		global __GCTHREAD_STOP_FLAG
		if __GCTHREAD_STOP_FLAG:
			break

def StopGCThreads():
	global __GCTHREAD_STOP_FLAG
	__GCTHREAD_STOP_FLAG = True

class RenderStats:
	def __init__(self):
		self.frameTime = 0.0
		self.updateTime = 0.0
		self.renderTime = 0.0
		self.eventHandlingTime = 0.0
		self.playgroundDrawTime = 0.0
		self.waitTime = 0.0

		self.blitCount = 0
	
	def Reset(self):
		self.blitCount = 0