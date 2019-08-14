import os
import requests

directory = os.getcwd()

try:
	f = open('version.txt', 'r')
except IOError:
	print("Unable to load file version.txt. Probably file is corrupted or doesn't exist.")
	q = None
	question = "Do you want to download the latest version? (Y/N): "
	while not any([q == 'y', q == 'Y', q == 'n', q =='N']):
		try: q = raw_input(question)
		except NameError: q = input(question)

		if q == 'Y' or q == 'y':
			Update(directory)
			break
		elif q == 'N' or q == 'n':
			quit()

version = f.readlines()
version = str(version[0])
f.close()

url_repo = "https://github.com/m4reQ/Oss-2.0/"
url_main = "https://github.com/m4reQ/Oss-2.0/master/osu!lool"
url_master = "https://github.com/m4reQ/Oss-2.0/master"

def Get_version():
	l, r = url_master[:8], url_master[8:]
	url = l + "raw." + r + "/version.txt"
	
	latest_version = requests.get(url)
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
	if version == str(late_ver):
		return
	else:
		print("Your version of the game is outdated.\nCurrent version: " + version + ".\nLatest version: " + late_ver)
		q = None
		question = "Do you want to download the latest version? (Y/N): "
		while not any([q == 'y', q == 'Y', q == 'n', q =='N']):
			try: q = raw_input(question)
			except NameError: q = input(question)

			if q == 'Y' or q == 'y':
				Update(directory)
				break
			elif q == 'N' or q == 'n':
				break
