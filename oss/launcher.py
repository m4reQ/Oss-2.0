try:
	import os
	import sys
except ImportError:
	print('Critical error! Cannot load os or sys module.')
	exit()

try:
	from helper import ask, logError, exitAll
	import repair
	from utils import resolutions, stats, ConvertImage, DimImage
	from Containers.texturecontainer import GenTexture, TextureContainer
	from Containers.soundcontainer import GenSound, SoundContainer
	from Containers.texturecontainer import SetDebugging as tcSetDebugging
	from Containers.soundcontainer import SetDebugging as scSetDebugging
	from GameElements.interface import SetDebugging as iSetDebugging
	from eventhandler import SetDebugging as ehSetDebugging
	import concurrent.futures
	import time
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
resolution = resolutions.SD

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
background_surf = None

#game window
mainWindow = None

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
	
	if sets.DEBUG_MODE:
		tcSetDebugging(True)
		scSetDebugging(True)
		iSetDebugging(True)
		ehSetDebugging(True)

def SetGameStats(ar, cs, hp):
	try:
		return (stats.clamp(ar), stats.clamp(cs), stats.clamp(hp))
	except Exception as e:
		logError(e)
		print('An error appeared during setting game stats.')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def InitializeTextureContainers():
	try:
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
		bg = pygame.Surface(resolution, pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL)#.convert_alpha()
		bg = bg.fill((0, 0, 0, int(darkenPercent*255)))
		dark = pygame.Surface(resolution, pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL)#.convert_alpha()
		dark.fill((0, 0, 0, darkenPercent*255))

		return (bg, dark)
	except Exception as e:
		logError(e)
		print('An error appeared during surfaces initialization. ')
		if sets.DEBUG_MODE:
			print('[ERROR] ', str(e))
		exitAll()

def LoadCircleTextures():
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

def LoadInterfaceTextures():
	#interface textures
	#check if textures was previously loaded
	if interfaceTextures.is_empty:
		interfaceTextures.AddTexture(GenTexture(tex_path + 'cursor.png', (16 * scale, 16 * scale)), 'cursor')
		interfaceTextures.AddTexture(GenTexture(tex_path + 'miss.png', (16 * scale, 16 * scale)), 'miss')

def LoadBackgroundTextures():
	#load backgrounds
	#check if textures was previously loaded
	if backgroundTextures.is_empty:
		#get names and number of files in backgrounds directory
		filenames = [name for name in os.listdir(os.path.join(tex_path, 'backgrounds')) if os.path.isfile(os.path.join(tex_path, 'backgrounds', name))]
		filenames.remove('Thumbs.db')
		jpgs = [os.path.join(tex_path, 'backgrounds', name) for name in filenames if name[-4:] != '.png']
		pngs = [os.path.join(tex_path, 'backgrounds', name) for name in filenames if name[-4:] != '.jpg']

		jpgNames = [name[:-4] for name in jpgs]
		pngNames = [name[:-4] for name in pngs]

		count_jpg = len(jpgs)

		#convert jpg images to png
		if sets.DEBUG_MODE:
			print('[INFO]<', str(__name__), '> Processing background images...')

		with concurrent.futures.ThreadPoolExecutor() as executor:
			for idx, tex in enumerate(jpgNames):
				if not tex in pngNames:
						executor.submit(ConvertImage, jpgs[idx])

		if sets.DEBUG_MODE:
			print('[INFO]<', str(__name__), '> Background images processing done.')

		#load backgrounds to backgroundTextures container
		for i in range(count_jpg-1):
			tex = GenTexture(tex_path + 'backgrounds/bg' + str(i) + '.png', resolution)
			backgroundTextures.AddTexture(tex, 'bg_' + str(i))

		#convert background textures to support alpha blending
		#and dim all of them
		for key in backgroundTextures.textures:
			tex = DimImage(backgroundTextures.textures[key], darkenPercent)
			backgroundTextures.textures[key] = tex

		backgroundTextures.AddTexture(GenTexture(tex_path + 'backgrounds/menu_background.png', resolution), 'menu_background')

def LoadTextures():
	try:
		with concurrent.futures.ThreadPoolExecutor() as executor:
			executor.submit(LoadBackgroundTextures)
			executor.submit(LoadCircleTextures)
			executor.submit(LoadInterfaceTextures)

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
	global AR, CS, HP
	AR, CS, HP = SetGameStats(5, 5, 5)

	#initialize sounds
	global hitsounds
	hitsounds = InitializeSoundContainers()
	LoadSounds()

	#initialize surfaces
	global background, dim
	background, dim = InitializeSurfaces()

	#initialize window
	global resolution, mainWindow
	mainWindow = InitializeWindow(resolution[0], resolution[1])

	#initialize textures
	global circleTextures, backgroundTextures, interfaceTextures
	circleTextures, backgroundTextures, interfaceTextures = InitializeTextureContainers()
	LoadTextures()

	#import menu module here to avoid cyclic import
	import menu

	try:
		if sets.TEST_MODE:
			raise Exception('[INFO] Test mode enabled.')

		if not sets.DEBUG_MODE:
			update.Check_version()

		if sets.DEBUG_MODE:
			print('[INFO]<', str(__name__), '> Program loaded in ', str(time.perf_counter() - start), ' seconds.')

		print('Welcome to Oss!')
	
		m = menu.Menu(mainWindow)
		m.Run()

	except Exception as e:
		logError(e)
		print('An error appeared. ', e)

	exitAll()
	