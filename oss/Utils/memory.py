if __name__ == "__main__":
    import sys
    sys.exit()

import gc

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