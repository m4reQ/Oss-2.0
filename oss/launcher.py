try:
	import os
	import sys
except ImportError:
	print('Critical error! Cannot load os or sys module.')
	exit()

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
except ImportError:
	print("Cannot import pygame!")

#create launcher infos to allow backward compatibility
#assume user uses python 3.x
class LauncherInfo:
	concurrencyAvailable = True
	timePerfCounterAvailable = True

#check if python supports modern concurrent execution
try:
	import concurrent.futures
except ImportError:
	LauncherInfo.concurrencyAvailable = False

#check if time module has function perf_counter
import time
if not 'perf_counter' in dir(time):
	LauncherInfo.timePerfCounterAvailable = False

#import internal modules
try:
	from helper import ask
	import repair
	from resourceManager import ResourceManager
	from texture import Texture
	from sound import Sound
	from utils import resolutions, stats, ConvertImage, DimImage, FreeMem
	import pygameWindow
	from pygameWindow import WindowFlags
	from settings import Settings
	import update
except ImportError:
	print("Error during importing internal modules")
	raise

#import external modules
try:
	import pygame
	import PIL
	import requests
	import wmi
	import pywin
except ImportError as e:
	print('Error! One of modules cannot be resolved.')

	if repair.CheckResponse():
		if ask("Do you want to launch the repair module?"):
			repair.InstallPackages()
	else:
		raise Exception('Error! Cannot use repair module.')
	
	raise

#check maps folder
if not os.path.exists('./Resources/maps'):
	print('Directory maps is missing. Creating directory.')

	try:
		os.mkdir('./Resources/maps')
	except OSError:
		print('Error! Cannot create directory.')

		raise

	print('Directory created.')

#indicates if program is running in debug mode
debugging = False

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#resolution
resolution = resolutions.SD

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

#background dimming
darkenPercent = 0.7

#master volume
mVolume = 0.55

#cursor size
curSize = 1.0

#####STATICS#####
#folder paths
texPath = 'Resources/textures/'
mapsPath = 'Resources/maps/'
soundsPath = 'Resources/sounds/'

#main settings container
sets = Settings()

#resource managers
mainResManager = ResourceManager("mainManager", 0)

#game window
mainWindow = None

#indicates if program is already initialized
initialized = False

#key bind table
keybind = {
'kl': None,
'kr': None}

def LoadSettings():
	try:
		global sets
		sets.LoadFromFile('settings.txt')
	except Exception as e:
		print("An error appeared during settings loading.")
		raise
	
	global debugging
	debugging = sets.DEBUG_MODE

def InitPygame():
	try:
		pygame.mixer.pre_init(22050, -16, 2, 512)
		pygame.mixer.init()
		pygame.init()
	except Exception as e:
		print("An error appeared during pygame initialization.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def SetKeyBindings():
	try:
		global keybind
		keybind['kl'] = pygame.K_z
		keybind['kr'] = pygame.K_x
	except Exception as e:
		print("An error appeared during loading key bindings.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def SetGameStats(ar, cs, hp):
	try:
		#clamp values
		ar = stats.clamp(ar)
		cs = stats.clamp(cs)
		hp = stats.clamp(hp)

		#convert stats to actual usable values
		return (stats.getAR(ar), stats.getCS(cs), stats.getHP(hp))
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
		pygame.mouse.set_visible(sets.mouse_visible)
		if sets.full_screen:
			win = pygameWindow.CreateWindow(width, height, "Oss!", WindowFlags.FullScreen | WindowFlags.DoubleBuf | WindowFlags.Accelerated)
		else:
			if sets.borderless:
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
		if LauncherInfo.concurrencyAvailable:
			with concurrent.futures.ThreadPoolExecutor() as executor:
				executor.submit(LoadBackgroundTextures)
				executor.submit(LoadCircleTextures)
				executor.submit(LoadInterfaceTextures)
		else:
			LoadBackgroundTextures()
			LoadCircleTextures()
			LoadInterfaceTextures()
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
	cursor.Scale(int(32 * curSize * scale))
	mainResManager.AddTexture("cursor", cursor)

	miss = Texture(texPath + 'miss.png')
	miss.Scale(16 * scale)
	mainResManager.AddTexture("miss", miss)

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

	if LauncherInfo.concurrencyAvailable:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			for idx, tex in enumerate(jpgNames):
				if not tex in pngNames:
					executor.submit(ConvertImage, jpgs[idx])
	else:
		for idx, tex in enumerate(jpgNames):
			if not tex in pngNames:
				ConvertImage(jpgs[idx])

	if debugging:
		print('[INFO]<{}> Background images processing done.'.format(__name__))

	for i in range(jpgCount - 1):
		texName = 'bg_' + str(i)

		tex = Texture("{}backgrounds/bg{}.png".format(texPath, i))
		tex.ScaleXY(resolution[0], resolution[1])
		tex.Dim(darkenPercent)
		mainResManager.AddTexture(texName, tex)

	menuBg = Texture(texPath + 'backgrounds/menu_background.png')
	menuBg.ScaleXY(resolution[0], resolution[1])
	mainResManager.AddTexture("menu_background", menuBg)

def LoadSounds():
	try:
		for i in range(1, 3):
			hitSound = Sound("{}hit{}.wav".format(soundsPath, i))
			hitSound.SetVolume(mVolume)
			mainResManager.AddSound("hit" + str(i), hitSound)

		miss = Sound(soundsPath + "miss.wav")
		miss.SetVolume(mVolume)
		mainResManager.AddSound("miss", miss)

		btn = Sound(soundsPath + "button_slide.wav")
		btn.SetVolume(mVolume)
		mainResManager.AddSound("button_slide", miss)

	except Exception as e:
		print("An error appeared during sounds loading.")
		if debugging:
			print('[ERROR]<{}> {}'.format(__name__, str(e)))
		
		raise

def Start():
	global initialized
	if initialized:
		raise Exception("Error! Program is already initialized.")

	#if perf_counter() is unavailable use less precise time.time() method
	start = time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time()

	#load settings
	LoadSettings() #from this point we can use debugging var instead of sets.DEBUG_MODE

	print('Initiaizing oss!')

	if debugging:
		if LauncherInfo.concurrencyAvailable:
			print('[INFO]<{}> Initialization started using multithereading.'.format(__name__))
		else:
			print('[INFO]<{}> Initialization started using singlethreading.'.format(__name__))

	#initialize pygame
	InitPygame()

	#load key bindings
	SetKeyBindings()

	#set game stats (AR, CS, HP)
	global AR, CS, HP
	AR, CS, HP = SetGameStats(AR_raw, CS_raw, HP_raw)

	#initialize window
	global mainWindow
	mainWindow = InitializeWindow(resolution[0], resolution[1])

	#initialize resources
	LoadTextures()
	LoadSounds()
	mainFont = pygame.font.SysFont('comicsansms', 22)
	mainResManager.AddMainFont(mainFont)
	mainResManager.AddFont("comicsansms_48", pygame.font.SysFont('comicsansms', 48))
	mainResManager.AddFont("comicsansms_24", pygame.font.SysFont('comicsansms', 24))
	mainResManager.AddFont("comicsansms_18", pygame.font.SysFont('comicsansms', 18))
	mainResManager.AddFont("comicsansms_12", pygame.font.SysFont('comicsansms', 12))

	if debugging:
		print("[INFO]<{}> Initialized resources. Memory reserved: {}kb. (approx.)".format(__name__, mainResManager.Size / 1000.0))

	#import menu module here to avoid circular import
	import menu

	#free memory after initialization
	FreeMem(debugging)

	try:
		if not debugging:
			update.Check_version()

		if debugging:
			print('[INFO]<{}> Program loaded in {} seconds.'.format(__name__, ((time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time()) - start)))

		initialized = True

		print('Welcome to Oss!')
	
		m = menu.Menu(mainWindow)
		m.Run()

		print('Goodbye!')

		if debugging:
			print('[INFO]<{}> Program exited after: {} miliseconds.'.format(__name__, m.time))
		
		pygame.mixer.quit()
		pygame.quit()

		FreeMem(debugging)
		
		os.system('pause >NUL')
		quit()

	except Exception as e:
		print('An error appeared. {}'.format(e))
		raise
	