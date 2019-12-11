try:
	import os
	import sys
except ImportError:
	print('Critical error! Cannot load os or sys module.')
	exit()

try:
	from helper import ask, logError, stats, Resolutions, exitAll
	import time
	import repair
	import matplotlib
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
		print('Error! Cannot use repair module.')
		exitAll()

	print('Module checking done. Please restart application.')
	exitAll()

#clear log file
with open('log.txt', 'w+') as logf:
	logf.write('')

#check maps folder
if not os.path.exists('./Resources/maps'):
	try:
		print('Directory maps is missing. Creating directory.')
		os.mkdir('./Resources/maps')
	except Exception as e:
		logError(e)
		print('Error! Cannot create directory.')

		exitAll()

#disable python warnings
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#resolution
resolution = Resolutions.SD

#target frame rate
#set 0 for unlimited
targetFPS = 60

#####GAME STATS#####
#circle approach rate
AR = None
#circle size
CS = None
#hp drop
HP = None

#background dimming
darkenPercent = 0.5

#master volume
mVolume = 0.55

#####STATICS#####
#textures folder path
tex_path = 'Resources/textures/'

#maps folder path
maps_path = 'Resources/maps/'

#sounds folder path
sounds_path = 'Resources/sounds/'

#settings container
sets = Settings()

#texture containers
circleTextures = None
backgroundTextures = None
interfaceTextures = None

#sound containers
hitsounds = None

#display surfaces
background = None
dim = None

#key bind table
keybind = {
'kl': None,
'kr': None,}

def LoadSettings():
	try:
		global sets
		sets.LoadFromFile('settings.txt')
	except Exception as e:
		logError(e)
		print('An error appeared during settings loading.')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def SetGameStats(ar, cs, hp):
	try:
		global AR, CS, HP

		if cs < 1:
			CS = 1
		elif cs > 10:
			CS = 10
		else:
			CS = cs

		if hp < 0:
			HP = 0
		elif hp > 10:
			HP = 10
		else:
			HP = hp

		AR = ar
	except Exception as e:
		logError(e)
		print('An error appeared during setting game stats.')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def InitializeTextureContainers():
	try:
		from texturecontainer import TextureContainer
		containers = (
			TextureContainer(name='circle'),
			TextureContainer(name='backgrounds'),
			TextureContainer(name='interface'))

		return containers
	except Exception as e:
		logError(e)
		print('An error appeared during texture containers initialization. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def InitializeSoundContainers():
	try:
		from soundcontainer import SoundContainer
		containers = (SoundContainer(name='hitsounds'))

		return containers
	except Exception as e:
		logError(e)
		print('An error appeared during sound containers initialization. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def InitializeSurfaces():
	try:
		bg = pygame.Surface(resolution, pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL).convert_alpha()
		dark = pygame.Surface(resolution, pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL).convert_alpha()
		dark.fill((0, 0, 0, darkenPercent*255))

		return (bg, dark)
	except Exception as e:
		logError(e)
		print('An error appeared during surfaces initialization. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()
def LoadTextures():
	try:
		from texturecontainer import GenTexture

		#circle radius
		radius = int(stats.getCS(CS) * scale)

		#circle textures
		#check if textures was previously loaded
		if circleTextures.is_empty:
			#load font textures
			for i in range(10):
				tex = GenTexture(tex_path + 'circles/' + str(i) + '.png', (radius*2, radius*2))
				circleTextures.AddTexture(tex, str('font_' + str(i)))
			#load background textures
			for i in range(5):
				tex = GenTexture(tex_path + 'circles/circlebg_' + str(i) + '.png', (radius*2, radius*2))
				circleTextures.AddTexture(tex, str('bg_' + str(i)))

		#interface textures
		#check if textures was previously loaded
		if interfaceTextures.is_empty:
			interfaceTextures.AddTexture(GenTexture(tex_path + 'cursor.png', (16 * scale, 16 * scale)), 'cursor')
			interfaceTextures.AddTexture(GenTexture(tex_path + 'miss.png', (16 * scale, 16 * scale)), 'miss')

			#load backgrounds
			#get number of files in backgrounds directory
			filesCount = len([name for name in os.listdir(os.path.join(tex_path, 'backgrounds')) if os.path.isfile(os.path.join(tex_path, 'backgrounds', name))])
			for i in range(filesCount - 1):
				tex = GenTexture(tex_path + 'backgrounds/bg' + str(i) + '.jpg', resolution)
				backgroundTextures.AddTexture(tex, 'bg_' + str(i-1))

		if not all([circleTextures.is_empty, interfaceTextures.is_empty, backgroundTextures.is_empty]):
			if sets.DEBUG_MODE:
				print('[INFO]<', str(__name__), "> Initialized textures. Texture dictionary: ", str(circleTextures.textures), str(interfaceTextures.textures), str(backgroundTextures.textures))

	except Exception as e:
		logError(e)
		print('An error appeared during textures loading. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def LoadSounds():
	try:
		from soundcontainer import GenSound
		global mVolume

		if hitsounds.is_empty:
			hitsounds.AddSound(GenSound(sounds_path + 'hit1.wav'), 'hit1')
			hitsounds.AddSound(GenSound(sounds_path + 'hit2.wav'), 'hit2')
			hitsounds.AddSound(GenSound(sounds_path + 'miss.wav'), 'miss')

		for s in hitsounds.sounds.values():
			s.set_volume(mVolume)

		if not hitsounds.is_empty:
			if sets.DEBUG_MODE:
				print('[INFO]<', str(__name__), "> Initialized sounds. Sounds dictionary: ", str(hitsounds.sounds))

	except Exception as e:
		logError(e)
		print('An error appeared during sounds loading. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def SetKeyBindings():
	try:
		global keybind

		keybind['kl'] = pygame.K_z
		keybind['kr'] = pygame.K_x
	except Exception as e:
		logError(e)
		print('An error appeared during loading key bindings. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def InitializeWindow(width, height):
	"""
	Initializes application window
	rtype: int, int
	returns: pygame.Surface
	"""

	try:
		pygame.mouse.set_visible(sets.mouse_visible)

		if sets.full_screen:
			try: 
				win = pygame.display.set_mode((width, height), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.HWACCEL)
			except Exception as e:
				print('Cannot set window, because resolution is too high.')
				logError(e)
		else:
			if sets.borderless:
				win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.NOFRAME|pygame.HWSURFACE|pygame.HWACCEL)
			if not sets.borderless:
				win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.HWACCEL)

		if sets.DEBUG_MODE:
			print('[INFO] Current display driver: ', pygame.display.get_driver())

		return win
	except Exception as e:
		logError(e)
		print('An error appeared during window initialization.')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def Start():
	start = time.perf_counter()

	#initialize pygame
	pygame.mixer.pre_init(22050, -16, 2, 512)
	pygame.mixer.init()
	pygame.init()

	#load settings
	LoadSettings()

	#load key bindings
	SetKeyBindings()

	#set game stats (AR, CS, HP)
	SetGameStats(5, 5, 5)

	#initialize textures
	global circleTextures, backgroundTextures, interfaceTextures
	circleTextures, backgroundTextures, interfaceTextures = InitializeTextureContainers()
	LoadTextures()

	#initialize sounds
	global hitsounds
	hitsounds = InitializeSoundContainers()
	LoadSounds()

	#initialize window
	global resolution
	mainWindow = InitializeWindow(resolution[0], resolution[1])

	#initialize surfaces
	global background, dim
	background, dim = InitializeSurfaces()

	#import game module here to avoid cyclic import
	import game

	try:
		if sets.TEST_MODE:
			raise Exception('[INFO] Test mode enabled.')

		if not sets.DEBUG_MODE:
			update.Check_version()

		print('Welcome to Oss!')
	
		g = game.Game(mainWindow)

		if sets.DEBUG_MODE:
			print('[INFO]<', str(__name__), '> Program loaded in ', str(time.perf_counter() - start), ' seconds.')

		g.Run()

	except Exception as e:
		logError(e)
		print(e)

	exitAll()
	