try:
    import os
    import sys
except ImportError:
    print('Critical error! Cannot load os or sys module.')
    os.system('pause >NUL')
    exit()

try:
    ext_modules = ['pygame', 'itertools']
    from helper import *
    from helper import logError
    import traceback
    import repair, update
    from eventhandler import *
    import time
    import random
    import concurrent.futures
    import pygame
    import pygame.locals
    import itertools
except ImportError as e:
    logError(e)
    print('Error! One of modules cannot be resolved. \nTry restarting your application or reinstalling it.')
    if repair.Check_response():
        if ask("Do you want to launch the repair module?"):
            repair.main(ext_modules)

    print('Module checking done.')

    os.system('pause >NUL')
    quit()

#disable python warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#clear log file
with open('log.txt', 'w+') as logf:
    logf.write('')

#####overall settings#####
try:
    sets = loadSettings('settings.txt')
except Exception as e:
    logError(e)
    print(e)

    pygame.quit()
    os.system("pause >NUL")
    quit()

sets = itertools.cycle(sets)

resolution = Resolutions.SD
full_screen = next(sets)
borderless = next(sets)
mouse_visible = next(sets)
auto_generate = next(sets)

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#background dimming
darken_percent = 0.2

#####developer settings#####
#NOTE!
#All developer settings are variables 
#in capital letters
DEBUG_MODE = next(sets)
TEST_MODE = next(sets)

#dictionary update mode
DICT_UPDATE_MODE = next(sets)

#use timed updates
timed_updates_enable = next(sets)

#use default display settings
defaultset = next(sets)

#####GAME STATS#####
#circle approach rate
AR = 5

#circle size
#min = 0, max = 10
CS = 5

#hp drop
#min = 0, max = 10
HP = 5

#####STATICS#####
#clock
clock = pygame.time.Clock()

#textures loading
cursor_texture = None
miss_texture = None
bg_texture = None

#surfaces initialization
bg_surf = None
dark = None

def Initialize_window(width, height):
    """
    Initializes application window
    rtype: int, int
    returns: pygame.Surface
    """
    global cursor_texture, miss_texture, bg_texture, bg_surf, dark, mouse_visible

    pygame.init()

    pygame.mouse.set_visible(mouse_visible)

    if full_screen:
        try: 
            win = pygame.display.set_mode((width, height), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.HWACCEL)
        except Exception as e:
            print('[ERROR] Cannot set window, because resolution is too high.')
            logError(e)

            pygame.quit()
            os.system("pause >NUL")
            quit()
            
    else:
        if borderless:
            win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.NOFRAME|pygame.HWSURFACE|pygame.HWACCEL)
        if not borderless:
            win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.HWSURFACE|pygame.HWACCEL)

    if DEBUG_MODE:
        print('[INFO] Current display driver: ' + pygame.display.get_driver())
    
    cursor_texture = pygame.image.load('textures/cursor.png')
    cursor_texture = pygame.transform.scale(cursor_texture, (int(16 * scale), int(16 * scale)))

    miss_texture = pygame.image.load('textures/miss.png')
    miss_texture = pygame.transform.scale(cursor_texture, (int(16 * scale), int(16 * scale)))

    bg_textures = []
    i = 1
    while i <= 9:
        string = 'bg' + str(i)
        bg_textures.append(string)
        i += 1

    texture_no = bg_textures[random.randint(0, len(bg_textures)-1)]
    bg_texture = pygame.image.load('textures/backgrounds/' + texture_no + '.jpg')
    bg_texture = pygame.transform.scale(bg_texture, (width, height))

    bg_surf = pygame.Surface((width, height), pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL).convert_alpha()
    
    dark = pygame.Surface(bg_texture.get_size(), pygame.HWSURFACE|pygame.SRCALPHA|pygame.HWACCEL).convert_alpha()
    dark.fill((0, 0, 0, darken_percent*255))

    return win

#called once to update window background
@run_once
def pre_update_display():
    pygame.display.update()

def timed_update_display():
    if DEBUG_MODE:
        print('[INFO] Updating screen.')
    pygame.display.update()

timed_update_display = run_interval(timed_update_display, 10)

#import internal modules
import circle, map, interface

class Game():
    def __init__(self, res):
        self.time = 0
        self.width, self.height = res
        self.win = Initialize_window(self.width, self.height)
        self.is_running = True
        self.click_count = [0, 0] #[0] stands for left key, [1] for right
        self.cursor_pos = (0, 0)
        self.circles = []
        self.playfield = {
        'topX': (self.width / 10 + int(stats.getCS(1) / 2)),
        'topY': (self.height / 10 + int(stats.getCS(1) / 2)),
        'bottomX': (self.width - self.width / 10 - int(stats.getCS(1) / 2)),
        'bottomY': (self.height - self.height / 10 - int(stats.getCS(1) / 2))}
        self.points = 0
        self.combo = 0
        self.maxhealth = 100
        self.health = self.maxhealth
        self.AR = AR
        self.CS = CS
        self.HP = HP
        self.render_time = 0
        self.fps = 0
        self.events = pygame.event.get()
        self.draw_interface = True
        self.toUpdate = []

        interface.setDebugMode()
        interface.changeFont('comicsansms', 48)

        self.cursor = interface.InterfaceElement(cursor_texture.get_width(), cursor_texture.get_height(), drawable=cursor_texture)
        self.combo_text = interface.InterfaceElement(0, 55, position=(10, self.height - 70), textColor=color.white)
        self.points_text = interface.InterfaceElement(0, 55, position=(0, self.height - 70), textColor=color.random())

        if self.CS < 1:
            self.CS = 1
        elif self.CS > 10:
            self.CS = 10

        if self.HP < 0:
            self.HP = 0
        elif self.HP > 10:
            self.HP = 10

    def Run(self):
        global DEBUG_MODE
        
        if not auto_generate:
            map_data = map.Load_map('test')
            self.circles = map.Make_map(map_data, (self.width, self.height))

            if type(self.circles).__name__ == 'str' or type(self.circles).__name__ == 'NoneType':
                raise Exception('[ERROR] An error appeared during map loading.')

                pygame.quit()
                os.system("pause >NUL")
                quit()
        
        radius = stats.getCS(1)

        while self.is_running:
            if auto_generate:
                if len(self.circles) < 1:
                    obj = circle.Circle(random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomX'] - radius)), random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomY'] - radius)))
                    self.circles.append(obj)

            self.events = pygame.event.get()

            if not self.circles:
                if DEBUG_MODE:
                    raise Exception('[INFO] List depleted at time: ' + str(self.time) + 'ms.' + '\n[INFO] Objects list self.circles is empty.')
                self.is_running = False

            #event handling
            for event in self.events: 
                self.cursor_pos = pygame.mouse.get_pos()

                if event.type == pygame.KEYDOWN:
                    EventHandler.HandleKeys(self, event, debug_mode=DEBUG_MODE)

                EventHandler.HandleEvents(self, event, debug_mode=DEBUG_MODE)

            if self.health <= 0:
                if DEBUG_MODE:
                    raise Exception('[INFO] self.health reached ' + str(self.health))
                self.is_running = False


            self.health -= stats.getHP(self.HP)
            
            if self.health >= self.maxhealth:
                self.health = self.maxhealth

            if DEBUG_MODE and len(self.circles) < 5:
                print('[INFO] ' + str(self.circles))
            if DEBUG_MODE and len(self.circles) >= 5:
                print('[INFO] Circle list Minimized. Contains: ' + str(len(self.circles))+ ' circles')

            #drawing section
            #NOTE!
            #Don't put anything below this section
            #it may cause glitches
            start = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.DrawPlayGround)
                if self.draw_interface:
                    executor.submit(self.DrawHealthBar)
                    executor.submit(self.DrawCursor)
                    executor.submit(self.DrawCombo)
                    executor.submit(self.DrawPoints)
                    executor.submit(self.DrawTime)
                    executor.submit(self.DrawClicksCounter)
                    if DEBUG_MODE:
                        executor.submit(self.DrawFPSCounter)
                executor.submit(self.DrawCursor)

            #####implement rects dictionary update here #####
            pre_update_display()

            if DICT_UPDATE_MODE:
                pygame.display.update(self.toUpdate)
                print('[INFO] Updating: ' + str(self.toUpdate))

                self.toUpdate.clear()

                if timed_updates_enable:
                    timed_update_display()
            #####end of implementation##### 
            if not DICT_UPDATE_MODE:
                pygame.display.flip()

            clock.tick(60)
            finish = time.perf_counter()

            self.fps = int(clock.get_fps())
            self.render_time = round(finish - start, 3)
            self.time = pygame.time.get_ticks()

    
    def DrawPlayGround(self):
        self.win.blit(bg_texture, (0, 0))
        self.win.blit(dark, (0, 0))

        for circle in self.circles:
            if not auto_generate: #in case of playing a map
                if self.time >= circle.time and self.time <= circle.time + stats.getAR(self.AR):
                    circle.Draw(self.win)  
                    for event in self.events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_z or pygame.K_x:
                                if circle.Collide(self.cursor_pos):
                                    circle.Hit(self)
                                else:
                                    circle.Miss(self)

                elif self.time >= circle.time + stats.getAR(self.AR):
                    circle.Miss(self)
            else: #in case of playing in auto generate mode
                circle.Draw(self.win)  
                for event in self.events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_z or event.key == pygame.K_x:
                            if circle.Collide(self.cursor_pos):
                                circle.Hit(self)
                            else:
                                circle.Miss(self)

    def DrawCursor(self):
        self.cursor.positionX = self.cursor_pos[0] - self.cursor.width/2
        self.cursor.positionY = self.cursor_pos[1] - self.cursor.height/2

        self.cursor.render(self.win)

        rect = self.cursor.getRect()

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

    def DrawCombo(self):
        interface.changeFont('comicsansms', 48)

        text = 'combo: ' + str(self.combo)

        self.combo_text.text = text
        self.combo_text.width = len(text) * 25

        self.combo_text.render(self.win)

        rect = self.cursor.getRect()

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

    def DrawPoints(self):
        text = 'points: ' + str(self.points)
        
        self.points_text.text = text
        self.points_text.width = len(text) * 24 - 5
        self.points_text.textPositionX = (self.width - len(text) * 24)

        self.points_text.render(self.win)

        rect = self.points_text.getRect()

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

    def DrawHealthBar(self):
        size_bg = (self.width - (2 * self.width/10), 30)
        pos = (self.width/10, 0)
        bar_bg = pygame.draw.rect(self.win, color.gray, (pos, size_bg))

        if self.health >= 0:
            if self.health <= self.maxhealth/5:
                c = color.red
            else:
                c = color.green
            size = ((self.playfield['bottomX'] - self.width/10) * self.health/self.maxhealth, 30)
            bar = pygame.draw.rect(self.win, c, (pos, size))

            rect = pygame.Rect((pos[0], pos[1]), (self.width - (2 * self.width/10), 30))

            if not rect in self.toUpdate:
                self.toUpdate.append(rect)

    def DrawTime(self):
        font = pygame.font.SysFont("comicsansms", 24)
        time = round((self.time/1000), 2)
        text = font.render('Time: ' + str(time) + 's', True, color.white)
        pos = (self.width/10, 0)

        self.win.blit(text, pos)

    def DrawClicksCounter(self):
        font = pygame.font.SysFont("comicsansms", 24)
        text_left = font.render(str(self.click_count[0]), True, color.white)
        text_right = font.render(str(self.click_count[1]), True, color.white)
        pos_left = ((self.width - (18*len(str(self.click_count[0])))), (self.height/2))
        pos_right = ((self.width - (18*len(str(self.click_count[1])))), (self.height/2 + 28))

        self.win.blit(text_left, pos_left)
        self.win.blit(text_right, pos_right)

    def DrawFPSCounter(self):
        font = pygame.font.SysFont("comicsansms", 12)
        text = 'Render time: ' + str(self.render_time) + 's | FPS: ' + str(self.fps)
        r_text = font.render(text, True, color.white)
        pos = (self.width - len(text) * 7, self.height - 80)

        max_length = (len(text)+2)

        self.win.blit(text, pos)

        rect = pygame.Rect((pos[0], pos[1]), (max_length * 7, 18))

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

if __name__ == '__main__':
    pygame.quit()
    quit()

#finish making clicks display and make background for it
#add miss animation (use image.alpha operations)
#change game behaviour to be used by menu as only a single game
#let various display settings to be read from settings file