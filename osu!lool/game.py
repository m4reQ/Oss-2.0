try:
    import os
    import sys
except ImportError:
    print('Critical error! Cannot load os or sys module.')
    os.system('pause >NUL')
    exit()

try:
    ext_modules = ['requests', 'pygame']
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    from helper import *
    import repair, update, circle, map
    import time
    import random
    import traceback
    import concurrent.futures
    import math
    import requests
    import pygame
    import pygame.locals
    import itertools
except ImportError:
    print('Error! One of modules cannot be resolved. \nTry restarting your application or reinstalling it.')
    if repair.Check_response():
        if ask("Do you want to launch the repair module?"):
            repair.main(ext_modules)
        else:
            pass
    print('Module checking done.')
    os.system('pause >NUL')
    with open('log.txt', 'w+') as logf:
            logf.write(traceback.format_exc())
            print(traceback.format_exc())
    quit()

#disable python warnings
if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

#####overall settings#####
sets = LoadSettings('settings.txt')
sets = itertools.cycle(sets)

resolution = Resolutions.SD
full_screen = next(sets)
borderless = next(sets)
defaultset = next(sets)
mouse_visible = next(sets)
auto_generate = next(sets)

#scale
#used to change size of objects depending on used resolution
#temporary set to 1 until making better method of calculating it
scale = 1

#background dimming
darken_percent = 0.9

#####developer settings#####
#NOTE!
#All developer settings are variables 
#in capital letters
DEBUG_MODE = next(sets)
TEST_MODE = next(sets)
UPDATE_MODE = next(sets)

#####GAME STATS#####
#circle approach rate
AR = 5

#circle size
#min = 0, max = 10
CS = 5

#hp drop
#min = 0, max = 10
HP = 5

#error log file
logf = open('log.txt', 'w+')

#####STATICS#####
#clock
clock = pygame.time.Clock()

#textures loading
cursor_texture = None
miss_texture = None
bg_texture = None

#surfaces initialization
bg_surf = None
pg_surf = None
dark = None

def Initialize_window(width, height):
    """
    Initializes application window
    rtype: int, int
    returns: pygame.Surface
    """
    global cursor_texture, miss_texture, bg_texture, bg_surf, pg_surf, dark, mouse_visible, scale

    if not defaultset:
        SetDisplaySettings()

    pygame.init()

    pygame.mouse.set_visible(mouse_visible)

    if full_screen:
        try: 
            win = pygame.display.set_mode((width, height), pygame.FULLSCREEN|pygame.DOUBLEBUF|pygame.HWSURFACE, 16)
        except Exception as e:
            print('[ERROR] Cannot set window, because resolution is too high.')
            with open('log.txt', 'w+') as logf:
                logf.write(traceback.format_exc())

            pygame.quit()
            os.system("pause >NUL")
            quit()
            
    else:
        if borderless:
            win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF|pygame.NOFRAME, 16)
        if not borderless:
            win = pygame.display.set_mode((width, height), pygame.DOUBLEBUF)
    
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

    bg_surf = pygame.Surface((width, height)).convert_alpha()
    pg_surf = pygame.Surface((width - (width/10), height - (height/9)))
    
    dark = pygame.Surface(bg_texture.get_size()).convert_alpha()
    dark.fill((0, 0, 0, darken_percent*255))

    return win

class Game():
    def __init__(self, res):
        self.time = 0
        self.width, self.height = res
        self.win = Initialize_window(self.width, self.height)
        self.is_running = True
        self.click_count = 0
        self.circles = []
        self.cursor_pos = (0, 0)
        self.playfield = {
        'topX': (self.width / 10 + int(stats.getCS(1) / 2)),                                                     #top X
        'topY': (self.height / 10 + int(stats.getCS(1) / 2)),                                                  #top Y
        'bottomX': (self.width - self.width / 10 - int(stats.getCS(1) / 2)),             #bottom X
        'bottomY': (self.height - self.height / 10 - int(stats.getCS(1) / 2))}        #bottom Y
        self.points = 0
        self.combo = 0
        self.combo_color = color.random()
        self.cursor_texture = cursor_texture
        self.miss_texture = miss_texture
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
                quit()
        else:
            pass
        
        radius = stats.getCS(self.CS)

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

            #key handling
            for event in self.events: 
                self.cursor_pos = pygame.mouse.get_pos()               
                if event.type == pygame.QUIT:
                    if DEBUG_MODE:
                        raise Exception('[INFO] User interruption by closing window')
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if DEBUG_MODE:
                            raise Exception('[INFO] User interruption by closing window')
                        self.is_running = False
                    if event.key == pygame.K_F10:
                        self.draw_interface = not self.draw_interface
                    #force screen update (ONLY IN DEBUG MODE)
                    if DEBUG_MODE:
                        if event.key == pygame.K_BACKQUOTE:
                            print('[INFO] Preformed window update.')
                            pygame.display.update()

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
                print('[INFO] Circle list Minimized. contains: ' + str(len(self.circles))+ ' circles')

            #drawing section
            #NOTE!
            #Don't put anything below this section
            #it may cause glitches
            start = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.DrawPlayGround)
                executor.submit(self.DrawCursor)
                if self.draw_interface:
                    executor.submit(self.DrawHealthBar)
                    executor.submit(self.DrawCursor)
                    executor.submit(self.DrawCombo)
                    executor.submit(self.DrawTime)
                    executor.submit(self.DrawClicksCounter)
                    if DEBUG_MODE:
                        executor.submit(self.DrawFPSCounter)

            #####implement rects dictionary update here #####
            if UPDATE_MODE:
                pygame.display.update(self.toUpdate)
                print('[INFO] Updating: ' + str(self.toUpdate))

                self.toUpdate.clear()
            #####end of implementation##### 
            if not UPDATE_MODE:
                pygame.display.flip()

            clock.tick()
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
                            if event.key == pygame.K_z or event.key == pygame.K_x:
                                if circle.Collide(self.cursor_pos):
                                    circle.Hit(self)
                                else:
                                    circle.Miss(self)

                                self.click_count += 1
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

                            self.click_count += 1

    def DrawCursor(self):
        self.win.blit(self.cursor_texture, (self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2))

        rect = pygame.Rect((self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2), (self.cursor_texture.get_width(),  self.cursor_texture.get_height()))

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

    def DrawCombo(self):
        font = pygame.font.SysFont("comicsansms", 48)
        text = 'points: ' + str(self.points)
        text_points = font.render(text, True, self.combo_color)
        text_combo = font.render('combo: ' + str(self.combo), True, color.white)
        length = len(text)

        self.win.blit(text_points, (self.width - length * 24, self.height - 70))
        self.win.blit(text_combo, (10, (self.height - 70)))

        rect = pygame.Rect((self.width - (length * 25 + 10), self.height - 58), (length * 48, self.height - (self.height - 58)))

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

            rect = pygame.Rect((self.width/10, 0), (self.width - (2 * self.width/10), 30))

            if not rect in self.toUpdate:
                self.toUpdate.append(rect)

    def DrawTime(self):
        font = pygame.font.SysFont("comicsansms", 24)
        time = round((self.time/1000), 2)
        text = font.render('Time: ' + str(time) + 's', True, color.white)
        pos = (self.width/10, 0)

        self.win.blit(text, pos)

        rect = pygame.Rect((pos[0], pos[1]), (len(text) * 24, 24))

        if not rect in self.toUpdate:
            self.toUpdate.append(rect)

    def DrawClicksCounter(self):
        font = pygame.font.SysFont("comicsansms", 24)
        text = font.render(str(self.click_count), True, color.white)
        pos = ((self.width - (18*len(str(self.click_count)))), (self.height/2))

        self.win.blit(text, pos)

    def DrawFPSCounter(self):
        font = pygame.font.SysFont("comicsansms", 12)
        string = 'Render time: ' + str(self.render_time) + 's | FPS: ' + str(self.fps)
        text = font.render(string, True, color.white)
        pos = (self.width - len(string) * 6, self.height - 80)

        self.win.blit(text, pos)

if __name__ == '__main__':
    try:
        if TEST_MODE:
            raise Exception('[INFO] Test mode enabled.')

        if not DEBUG_MODE:
            update.Check_version()
        
        g = Game(resolution)

        g.Run()

        pygame.quit()
        os.system("pause >NUL")
        quit()

    except Exception as e:
        if not str(e)[:6] == '[INFO]':
            with open('log.txt', 'w+') as logf:
                logf.write(traceback.format_exc())

        print(e)

        pygame.quit()
        os.system("pause >NUL")
        quit()
    
#finish making clicks display and make background for it
#add miss animation (use image.alpha operations)
#improve performance/make more Surfaces
#change game behaviour to be used by menu as only a single game
