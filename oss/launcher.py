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

#disable pygame welcome prompt
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#create launcher infos to allow backward compatibility
#assume user uses python 3.x
class LauncherInfo:
	concurrencyAvailable = True
	timePerfCounterAvailable = True

	@staticmethod
	def GetInfo(file=""):
		info = "LauncherInfo\n"

		for e in dir(LauncherInfo):
			if e[0] != '_' and e[1] != '_':
				info += "{}: {}\n".format(e, getattr(LauncherInfo, e))
		
		if not file:
			return info
		else:
			with open(file, "w+") as f:
				f.write(info)

#check if python supports modern concurrent execution
try:
	import concurrent.futures
except ImportError:
	LauncherInfo.concurrencyAvailable = False

#check if time module has function perf_counter
import time
if not 'perf_counter' in dir(time):
	LauncherInfo.timePerfCounterAvailable = False

try:
	from helper import ask, logError, exitAll
	import repair

	from resourceManager import ResourceManager
	from texture import Texture
	from sound import Sound

	from utils import resolutions, stats, ConvertImage, DimImage, FreeMem
	from eventhandler import SetDebugging as ehSetDebugging
	from GameElements.map import SetDebugging as mSetDebugging
	import pygameWindow
	from pygameWindow import WindowFlags
	import pygame
	from settings import Settings
	import update
except ImportError as e:
	logError(e)
	print('Error! One of modules cannot be resolved.')

	if repair.Check_response():
		if ask("Do you want to launch the repair module?"):
			repair.main()
	else:
		raise Exception('Error! Cannot use repair module.')

	exitAll()

#clear log file
open('log.txt', 'w+').close()

#check maps folder
if not os.path.exists('./Resources/maps'):
	print('Directory maps is missing. Creating directory.')
	try:
		os.mkdir('./Resources/maps')
	except Exception as e:
		logError(e)
		print('Error! Cannot create directory.')

		exitAll()
	print('Directory created.')

#indicates if program was already initialized
initialized = False

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
maps_path = 'Resources/maps/'
soundsPath = 'Resources/sounds/'

#main settings container
sets = Settings()

#resource managers
mainResManager = ResourceManager("mainManager", 0)

#game window
mainWindow = None

#key bind table
keybind = {
'kl': None,
'kr': None,
}

def LoadSettings():
	try:
		global sets
		sets.LoadFromFile('settings.txt')
	except Exception as e: #we cannot use HandleError here because it requires sets.DEBUG_MODE variable
		logError(e)
		print("An error appeared during settings loading.")
		if sets.DEBUG_MODE:
			print('[ERROR] {}'.format(str(e)))
		exitAll()
	
	# if sets.DEBUG_MODE:
	# 	tcSetDebugging(True)
	# 	scSetDebugging(True)
	# 	ehSetDebugging(True)
	# 	mSetDebugging(True)

def HandleError(msg, error):
	"""
	Performs a set of actions to properly catch error
	:param msg: (str) Error message to display
	:param error: (Exception) Actual catched error
	"""
	logError(error)
	print(msg)
	if sets.DEBUG_MODE:
		print('[ERROR] {}'.format(str(error)))
	exitAll()

def SetGameStats(ar, cs, hp):
	try:
		#clamp values
		ar = stats.clamp(ar)
		cs = stats.clamp(cs)
		hp = stats.clamp(hp)

		#convert stats to actual usable values
		return (stats.getAR(ar), stats.getCS(cs), stats.getHP(hp))
	except Exception as e:
		HandleError("An error appeared during setting game stats.", e)

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
	if sets.DEBUG_MODE:
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

	if sets.DEBUG_MODE:
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
		HandleError("An error appeared during textures loading.", e)

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
		HandleError("An error appeared during sounds loading.", e)

def SetKeyBindings():
	try:
		global keybind

		keybind['kl'] = pygame.K_z
		keybind['kr'] = pygame.K_x
	except Exception as e:
		HandleError("An error appeared during loading key bindings.", e)

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

		if sets.DEBUG_MODE:
			print('[INFO]<{}> Current display driver: {}.'.format(__name__, pygame.display.get_driver()))

		return win
	except Exception:
		HandleError("An error appeared during window initialization.", e)

def InitPygame():
	try:
		pygame.mixer.pre_init(22050, -16, 2, 512)
		pygame.mixer.init()
		pygame.init()
	except Exception as e:
		HandleError("An error appeared during pygame initialization.", e)

def Start():
	global initialized
	if initialized:
		raise Exception("Error! Program is already initialized.")

	#if perf_counter() is unavailable use less precise time.time() method
	start = (time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time())

	#load settings
	LoadSettings()

	print('Initiaizing oss!')
	if sets.DEBUG_MODE:
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
	mainResManager.AddFont("comicsansms_12", pygame.font.SysFont('comicsansms', 12))

	print("[INFO]<{}> Initialized resources. Memory reserved: {}kb. (approx.)".format(__name__, mainResManager.Size / 1000.0))

	#import menu module here to avoid cyclic import
	import menu

	#free memory after initialization
	FreeMem(sets.DEBUG_MODE)

	try:
		if sets.TEST_MODE:
			raise Exception('[INFO] Test mode enabled.')

		if not sets.DEBUG_MODE:
			update.Check_version()

		if sets.DEBUG_MODE:
			print('[INFO]<{}> Program loaded in {} seconds.'.format(__name__, ((time.perf_counter() if LauncherInfo.timePerfCounterAvailable else time.time()) - start)))

		initialized = True

		print('Welcome to Oss!')
	
		m = menu.Menu(mainWindow)
		m.Run()

		print('Goodbye!')

		if sets.DEBUG_MODE:
			print('[INFO]<{}> Program exited after: {} miliseconds.'.format(__name__, m.time))
		
		pygame.mixer.quit()
		pygame.quit()

		FreeMem(sets.DEBUG_MODE)
		
		os.system('pause >NUL')
		quit()

	except Exception as e:
		logError(e)
		print('An error appeared. {}'.format(e))
	