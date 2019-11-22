import os
from helper import ask
import requests

directory = os.getcwd()

try:
	f = open('version.txt', 'r')
except IOError:
	print("Unable to load file version.txt. Probably file is corrupted or doesn't exist.")
	if ask("Do you want to download the latest version? (Y/N): "):
		Update(directory)
	else:
		quit()

version = f.readlines()
version = str(version[0])
f.close()

url_repo = "https://github.com/m4reQ/Oss-2.0/"
url_main = "https://github.com/m4reQ/Oss-2.0/master/oss"
url_master = "https://github.com/m4reQ/Oss-2.0/master"

def Get_version():
	"""
	rtype: none
	returns: string or bool
	"""
	l, r = url_main[:8], url_main[8:]
	url = l + "raw." + r + "/version.txt"
	
	try:
		latest_version = requests.get(url)
	except requests.exceptions.ConnectionError:
		print('Cannot download latest version. Check your internet connection.')
		return False

	latest_version = str(latest_version.text)
	latest_version = latest_version[:11]

	return latest_version

def Update(dir):
	path = os.path.join(dir, 'tmp')
	
	files = os.listdir(path)
	for f in files:
		os.remove(os.path.join(path, f))

	url = url_repo + "/archive/master.zip"

	os.system("start \"\"" + " " + url)

def Check_version():
	late_ver = Get_version()
	if not late_ver:
		print("Couldn't update game.")
		return
	if not float(version) == float(late_ver):
		print("Your version of the game is outdated.\nCurrent version: " + version + ".\nLatest version: " + late_ver + '.')
		if ask("Do you want to download the latest version?"):
			Update(directory)
		else:
			pass
