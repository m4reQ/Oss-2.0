if __name__ == "__main__":
    import sys
    sys.exit()

import gc

try:
	from time import perf_counter as timer
except (ImportError, ModuleNotFoundError):
	from time import time as timer

__GCTHREAD_STOP_FLAG = False

def FreeMem(useDebugging, msg='Starting garbage collection'):
	"""
	Triggers garbage collection.
	:param useDebugging: (bool) tells if function should indicate a call
	:param msg: (str) message to display before starting GC
	"""

	try:
		objectsCount = gc.get_count()[0]
		if useDebugging:
			print('[INFO]<{}> {}.'.format(__name__, msg))
		gc.collect()
		if useDebugging:
			print('[INFO]<{}> Freed {} objects.'.format(__name__, objectsCount - gc.get_count()[0]))
	except Exception as e:
		print('[ERROR]<{}> An error occured during garbage collection. \n{}'.format(__name__, str(e)))

def TimedGarbageCollect(interval):
	while True:
		objectsCount = gc.get_count()[0]
		gc.collect()
		print('[INFO]<{}> GC thread freed {} objects.'.format(__name__, objectsCount - gc.get_count()[0]))
		time.sleep(interval)
		global __GCTHREAD_STOP_FLAG
		if __GCTHREAD_STOP_FLAG:
			break

def StopGCThreads():
	global __GCTHREAD_STOP_FLAG
	__GCTHREAD_STOP_FLAG = True

class Profiler:
	def __init__(self):
		self.profiledFrames = 0
		self.profiledTime = 0
		self.profiledMinFps = None
		self.profiledMaxFps = 0

		self.used = False
	
	def Profile(self, frameTime):
		self.used = True

		self.profiledTime += frameTime
		fps = (1.0 / frameTime)

		if fps > self.profiledMaxFps:
			self.profiledMaxFps = fps

		if self.profiledMinFps:
			if fps < self.profiledMinFps:
				self.profiledMinFps = fps
		else:
			self.profiledMinFps = fps

		self.profiledFrames += 1
	
	def GetProfileData(self):
		return "[INFO]<{}> Profiling was running for {} seconds ({} frames). FPS: max. {}, min. {}, avg. {}".format(__name__, self.profiledTime, self.profiledFrames, self.profiledMaxFps, self.profiledMinFps, 1.0 / (self.profiledTime / self.profiledFrames))

	def SaveProfileData(self, file):
		with open(file, "a") as f:
			f.write(self.GetProfileData() + "\n")