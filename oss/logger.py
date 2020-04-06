if __name__ == "__main__": quit()

import time
from datetime import datetime
import sys
import os

class Logger(object):
	class LExc(BaseException):
		__module__ = None
	
	maxLogFileLength = 100

	logFile = "log.txt"

	@classmethod
	def Set(cls, setting, value):
		try:
			if value != True and value != False:
				raise LExc

			cls.settings[setting] = value

		except KeyError:
			print(f"Invalid key: {setting}")
		except LExc:
			print(f"Invalid value: {value}")

	@classmethod
	def getLogFileLength(cls):
		return sum(1 for line in open(Logger.logFile, "r"))

	@classmethod
	def Log(cls, msg):
		if not os.path.isfile(Logger.logFile):
			open(Logger.logFile, "w+").close()

		with open(Logger.logFile, "a") as f:
			if Logger.getLogFileLength() > Logger.maxLogFileLength:
				f.truncate(0)

			f.write(msg + "\n")

def logged(func):
	def wrapper(*args, **kwargs):
		timestamp = datetime.now()
		caller = sys._getframe(0).f_back.f_code.co_name
		exception = ""
		end = 0.0

		start = time.time()
		try:
			rv = func(*args, **kwargs)
		except Exception as e:
			exception = f"'{e}'"
		finally:
			end = time.time()

		args = [str(arg) for arg in args]
		kwargs = [str(kwarg) for kwarg in kwargs]

		Logger.Log(f"[{func}] Caller: {caller} | Args: {', '.join(args)}, {', '.join(kwargs)} | Returns: {rv} | Call timestamp: {timestamp} | Exec time: {end - start}s | Exception: {exception}")

		return rv

	return wrapper