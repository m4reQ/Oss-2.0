#if it's available use most accurate time measurement
try:
	from time import perf_counter as timer
except (ImportError, ModuleNotFoundError):
	from time import time as timer
	
start = timer()

import os
import sys

#disable python warnings
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")

#route error output to file
sys.stderr = open('log.txt', 'w+')

#suppress pygame welcome message, import pygame
#and handle errors
try:
	oldStdout = sys.stdout
	sys.stdout = open(os.devnull, 'w')
	import pygame
	sys.stdout = oldStdout
except (ImportError, ModuleNotFoundError):
	print("Cannot import pygame.")

#import external modules
try:
	import pygame
	import PIL
	import requests
	import wmi
	import pywin
	import threading
except (ImportError, ModuleNotFoundError):
	import repair
	from Utils.other import Ask
	print('Error! One of modules cannot be resolved.')

	if repair.CheckResponse():
		if Ask("Do you want to launch the repair module?"):
			repair.InstallPackages()
	else:
		raise Exception('Error! Cannot use repair module.')
	
	raise

#import internal modules
try:
	import repair
	from resourceManager import ResourceManager
	from texture import Texture
	from sound import Sound
	from Utils.graphics import Resolutions, ConvertImage, DimImage, GetScale, GetScalingFactor
	from Utils.performance import FreeMem, TimedGarbageCollect, StopGCThreads
	from Utils.game import Stats
	from Utils.other import Ask
	from preferencies import Preferencies
	import pygameWindow
	from pygameWindow import WindowFlags
	import update
except ImportError:
	print("Error during importing internal modules")
	raise

#check maps folder
if not os.path.exists('./Resources/maps'):
	print('Directory maps is missing. Creating directory.')

	try:
		os.mkdir('./Resources/maps')
		os.mkdir('./Resources/maps/editor')
	except OSError:
		print('Error! Cannot create directories.')

		raise

	print('Directory created.')

#indicates if program is running in debug mode
debugging = False

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#user preferencies
prefs = None

#####GAME STATS#####
#circle approach rate
AR = None
#circle size
CS = None
#hp drop
HP = None

#raw stats
AR_raw = 5
CS_raw = 5
HP_raw = 5

#####STATICS#####
#folder paths
texPath = 'Resources/textures/'
mapsPath = 'Resources/maps/'
soundsPath = 'Resources/sounds/'

#resource managers
mainResManager = ResourceManager("mainManager", 0)

#game window
mainWindow = None

def LoadPreferencies():
	try:
		global prefs
		prefs = Preferencies.ImportFromFile(Preferencies.PREFS_FILE)
	except Exception as e:
		print("An error appeared during user preferencies loading.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))

		raise

def InitPygame():
	try:
		pygame.mixer.pre_init(22050, 16, 2, 512)
		pygame.mixer.init(allowedchanges=pygame.AUDIO_ALLOW_ANY_CHANGE)
		pygame.init()
	except Exception as e:
		print("An error appeared during pygame initialization.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def SetGameStats(ar, cs, hp):
	try:
		#clamp values
		ar = Stats.Clamp(ar)
		cs = Stats.Clamp(cs)
		hp = Stats.Clamp(hp)

		#convert stats to actual usable values
		return (Stats.GetAR(ar), Stats.GetCS(cs), Stats.GetHP(hp))
	except Exception as e:
		print("An error appeared during initializing game stats.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))

		raise

def InitializeWindow(width, height):
	"""
	Initializes application window
	rtype: int, int
	returns: pygame.Surface
	"""
	try:
		pygame.mouse.set_visible(prefs.mouseVisible)
		if prefs.fullscreen:
			win = pygameWindow.CreateWindow(width, height, "Oss!", WindowFlags.FullScreen | WindowFlags.DoubleBuf | WindowFlags.Accelerated)
		else:
			if prefs.borderless:
				win = pygameWindow.CreateWindow(width, height, "Oss!", WindowFlags.BorderLess | WindowFlags.DoubleBuf | WindowFlags.Accelerated)
			else:
				win = pygameWindow.CreateWindow(width, height,"Oss!",  WindowFlags.DoubleBuf | WindowFlags.Accelerated)

		if debugging:
			print('[INFO]<{}> Current display driver: {}.'.format(__name__, pygame.display.get_driver()))

		return win
	except Exception as e:
		print("An error appeared during window initialization.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def LoadTextures():
	try:
		texLoadThreads = [
			threading.Thread(name="BgTexLoadThread", target=LoadBackgroundTextures),
			threading.Thread(name="CircleTexLoadThread", target=LoadCircleTextures),
			threading.Thread(name="InterfaceTexLoadThread", target=LoadInterfaceTextures)]

		for thread in texLoadThreads:
			thread.start()
		
		for thread in texLoadThreads:
			thread.join()

	except Exception as e:
		print("An error appeared during textures loading.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def LoadCircleTextures():
	radius = int(CS * scale)

	for i in range(10):
		texName = 'circlefont_' + str(i)

		tex = Texture("{}circles/{}.png".format(texPath, i))
		tex.Scale(radius * 2 * scale)
		mainResManager.AddTexture(texName, tex)

	for i in range(5):
		texName = 'circlebg_'+ str(i)

		tex = Texture("{}circles/circlebg_{}.png".format(texPath, i))
		tex.Scale(radius * 2 * scale)
		mainResManager.AddTexture(texName, tex)

	circleHit = Texture(texPath + "circles/circlehit.png")
	circleHit.Scale(radius* 2 * scale)
	mainResManager.AddTexture("hitlayout", circleHit)

def LoadInterfaceTextures():
	cursor = Texture(texPath + 'cursor.png')
	cursor.Scale(int(32 * prefs.cursorSize * scale))
	mainResManager.AddTexture("cursor", cursor)

	miss = Texture(texPath + 'miss.png')
	miss.Scale(16 * scale)
	mainResManager.AddTexture("miss", miss)

	setsIcn = Texture(texPath + 'settingsIcon.png')
	setsIcn.Scale(48 * scale)
	mainResManager.AddTexture('setsIcn', setsIcn)

def LoadBackgroundTextures():
	#get names and number of files in backgrounds directory
	filenames = [name for name in os.listdir(os.path.join(texPath, 'backgrounds')) if os.path.isfile(os.path.join(texPath, 'backgrounds', name))]

	#remove Thumbs.db from filename list if it's present
	try: filenames.remove('Thumbs.db')
	except ValueError: pass

	#get all images
	jpgs = [os.path.join(texPath, 'backgrounds', name) for name in filenames if name[-4:] != '.png']
	pngs = [os.path.join(texPath, 'backgrounds', name) for name in filenames if name[-4:] != '.jpg']

	#get all names without .jpg or .png
	jpgNames = [name[:-4] for name in jpgs]
	pngNames = [name[:-4] for name in pngs]

	jpgCount = len(jpgs)

	#convert jpg images to png
	if debugging:
		print('[INFO]<{}> Processing background images...'.format(__name__))

	for idx, tex in enumerate(jpgNames):
		if not tex in pngNames:
			threading.Thread(target=ConvertImage, args=(jpgs[idx],)).start()

	if debugging:
		print('[INFO]<{}> Background images processing done.'.format(__name__))

	for i in range(jpgCount - 1):
		texName = 'bg_' + str(i)

		tex = Texture("{}backgrounds/bg{}.png".format(texPath, i))
		tex.ScaleXY(prefs.resolution[0], prefs.resolution[1])
		tex.Dim(prefs.darkenPercent)
		mainResManager.AddTexture(texName, tex)

	menuBg = Texture(texPath + 'backgrounds/menu_background.png')
	menuBg.ScaleXY(prefs.resolution[0], prefs.resolution[1])
	mainResManager.AddTexture("menu_background", menuBg)

def LoadSounds():
	try:
		for i in range(1, 3):
			hitSound = Sound("{}hit{}.wav".format(soundsPath, i))
			hitSound.SetVolume(prefs.masterVolume)
			mainResManager.AddSound("hit" + str(i), hitSound)

		miss = Sound(soundsPath + "miss.wav")
		miss.SetVolume(prefs.masterVolume)
		mainResManager.AddSound("miss", miss)

		btn = Sound(soundsPath + "button_slide.wav")
		btn.SetVolume(prefs.masterVolume)
		mainResManager.AddSound("button_slide", miss)

	except Exception as e:
		print("An error appeared during sounds loading.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def Start(debugMode):
	global debugging
	debugging = debugMode

	#load prefs
	LoadPreferencies()

	#set scaling factor (for now doesn't work)
	global scale
	scale = GetScalingFactor(GetScale(prefs.resolution[0], prefs.resolution[1]))
	if scale != 1:
		scale = 1

	print('Initiaizing oss!')

	#initialize pygame
	InitPygame()

	if prefs.lockMouse:
		pygame.event.set_grab(True)

	#set used SDL events
	pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION])

	#set game stats (AR, CS, HP)
	global AR, CS, HP
	AR, CS, HP = SetGameStats(AR_raw, CS_raw, HP_raw)

	#initialize window
	global mainWindow
	mainWindow = InitializeWindow(prefs.resolution[0], prefs.resolution[1])

	#initialize resources
	LoadTextures()
	LoadSounds()
	mainFont = pygame.font.SysFont('comicsansms', 22 * scale)
	mainResManager.AddMainFont(mainFont)
	mainResManager.AddFont("comicsansms_48", pygame.font.SysFont('comicsansms', 48 * scale))
	mainResManager.AddFont("comicsansms_24", pygame.font.SysFont('comicsansms', 24 * scale))
	mainResManager.AddFont("comicsansms_22", pygame.font.SysFont("comicsansms", 22 * scale))
	mainResManager.AddFont("comicsansms_21", pygame.font.SysFont("comicsansms", 21 * scale))
	mainResManager.AddFont("comicsansms_18", pygame.font.SysFont('comicsansms', 18 * scale))
	mainResManager.AddFont("comicsansms_12", pygame.font.SysFont('comicsansms', 12 * scale))
	mainResManager.AddFont("comicsansms_10", pygame.font.SysFont("comicsansms", 10 * scale))

	#import menu module here to avoid circular import
	import menu

	#free memory after initialization
	FreeMem(debugging)

	try:
		if debugging:
			print('[INFO]<{}> Program loaded in {} seconds.'.format(__name__, timer() - start))

		initialized = True

		print('Welcome to Oss!')
	
		m = menu.Menu(mainWindow)
		m.Run()

		print('Goodbye!')

		if debugging:
			print('[INFO]<{}> Program exited after: {} seconds.'.format(__name__, m.time))
		
		pygame.mixer.quit()
		pygame.quit()

		FreeMem(debugging)
		StopGCThreads()
		
		os.system('pause >NUL')
		sys.exit()

	except Exception as e:
		print('An error appeared. {}'.format(e))
		raise
	