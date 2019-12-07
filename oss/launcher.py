try:
	import os
	import sys
except ImportError:
	print('Critical error! Cannot load os or sys module.')
	exit()

try:
	ext_modules = ['pygame', 'requests']
	import repair
	from helper import ask, logError, stats
	import pygame
	from settings import Settings
	import update
except ImportError as e:
	logError(e)
	print('Error! One of modules cannot be resolved. \nTry restarting your application or reinstalling it.')

	if repair.Check_response():
		if ask("Do you want to launch the repair module?"):
			repair.main(ext_modules)
	else:
		print('Error! Cannot use repair module.')

		os.system('pause >NUL')
		quit()

	print('Module checking done. Please restart application.')

	os.system('pause >NUL')
	quit()

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

		os.system('pause >NUL')
		pygame.quit()
		quit()

#disable python warnings
if not sys.warnoptions:
	import warnings
	warnings.simplefilter("ignore")

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#####GAME STATS#####
#circle approach rate
AR = None
#circle size
CS = None
#hp drop
HP = None

#background dimming
darken_percent = 0.5

#####STATICS#####
#textures folder path
tex_path = 'Resources/textures/'

#maps folder path
maps_path = 'Resources/maps/'

#sounds folder path
sounds_path = 'Resources/sounds/'

#settings container
sets = Settings()

try:
	sets.LoadFromFile('settings.txt')
except Exception as e:
	logError(e)
	print(e)

	pygame.quit()
	os.system("pause >NUL")
	quit()

#texture containers
circleTextures = None
backgroundTextures = None
interfaceTextures = None

#sound containers
hitsounds = None

#key bind table
keybind = {
'kl': None,
'kr': None,}

def SetGameStats(ar, cs, hp):
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

def InitializeTextureContainers():
	from texturecontainer import TextureContainer
	containers = (
		TextureContainer(name='circle'),
		TextureContainer(name='backgrounds'),
		TextureContainer(name='interface'))

	return containers

def InitializeSoundContainers():
	from soundcontainer import SoundContainer
	containers = (SoundContainer(name='hitsounds'))

	return containers

def LoadTextures():
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

	if not circleTextures.is_empty:
		if sets.DEBUG_MODE:
			print('[INFO]<', str(__name__), "> Initialized circle textures. Texture dictionary: ", str(circleTextures.textures))

def LoadSounds():
	from soundcontainer import GenSound

	hitsounds.AddSound(GenSound(sounds_path + 'hit1.wav'), 'hit1')
	hitsounds.AddSound(GenSound(sounds_path + 'hit2.wav'), 'hit2')
	hitsounds.AddSound(GenSound(sounds_path + 'miss.wav'), 'miss')

	for s in hitsounds.sounds.values():
		s.set_volume(0.4)

def SetKeyBindings():
	global keybind

	keybind['kl'] = pygame.K_z
	keybind['kr'] = pygame.K_x

def Start():
	#initialize pygame
	pygame.mixer.pre_init(22050, -16, 2, 512)
	pygame.mixer.init()
	pygame.init()

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

	#load key bindings
	SetKeyBindings()

	#import game module here to avoid cyclic import
	import game

	try:
		if sets.TEST_MODE:
			raise Exception('[INFO] Test mode enabled.')

		if not sets.DEBUG_MODE:
			update.Check_version()

		print('Welcome to Oss!')
	
		g = game.Game(game.resolution)

		g.Run()

	except Exception as e:
		logError(e)
		print(e)

	pygame.mixer.quit()
	pygame.quit()
	os.system("pause >NUL")
	quit()
	