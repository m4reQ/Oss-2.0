import os
from helper import ask, logError, exitAll
import requests

directory = os.getcwd()

def Update(dir):
	path = os.path.join(dir, 'tmp')
	
	files = os.listdir(path)
	for f in files:
		os.remove(os.path.join(path, f))

	url = url_repo + "/archive/master.zip"

	os.system("start \"\"" + " " + url)

try:
	f = open('version.txt', 'r')
except IOError as e:
	print("[ERROR] Unable to load file version.txt. Probably file is corrupted or doesn't exist.")
	logError(e)
	
	if ask("Do you want to download the latest version?"):
		Update(directory)
	else:
		quit()

#get local version
version = f.readlines()
version = str(version[0])
f.close()

#urls
url_repo = "https://github.com/m4reQ/Oss-2.0/"
url_main = "https://github.com/m4reQ/Oss-2.0/master/oss"
url_master = "https://github.com/m4reQ/Oss-2.0/master"

def Get_version():
	"""
	gets newest version
	returns: string or bool
	"""
	l, r = url_main[:8], url_main[8:]
	url = l + "raw." + r + "/version.txt"
	
	try:
		latest_version = requests.get(url)
	except requests.exceptions.ConnectionError:
		print('[ERROR] Cannot download latest version. Check your internet connection.')
		return False

	latest_version = str(latest_version.text)
	latest_version = latest_version[:11]

	return latest_version

def Check_version():
	late_ver = Get_version()
	if not late_ver:
		print("Couldn't update game.")
	if not float(version) == float(late_ver):
		print('Your version of the game is outdated.\nCurrent version: {}.\nLatest version: {}.'.format(version, late_ver))
		if ask("Do you want to download the latest version?"):
			Update(directory)

if __name__ == '__main__':
	exitAll()