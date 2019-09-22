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
    import repair, update, circle, map
    from helper import *
    import time
    import random
    import traceback
    import concurrent.futures
    import math
    import requests
    import pygame
except ImportError:
    print('Error! One of modules cannot be resolved. \nTry restarting your application or reinstalling it.')
    if repair.Check_response():
        if ask("Do you want to launch the repair module?"):
            repair.main(ext_modules)
        else:
            pass
    print('Module checking done.')
    os.system('pause >NUL')
    exit()

#####overall settings#####

#resolution
resolution = resolutions['SD']

#fullscreen
full_screen = False

#background dimming
darken_percent = 0.50

#mouse visibility
mouse_visible = False

#####GAME STATS#####
#circle approach rate
AR = 5

#circle size
MIN_CS = 1
MAX_CS = 10
CS = 4

#hp drop
MIN_HP = 0
MAX_HP = 10
HP = 10

#automatic circle generation
auto_generate = True

#error log file
logf = open('log.txt', 'w+')

#debug mode
DEBUG_MODE = False
DEBUG_EXCEPTION = ''

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
    rtype: int, int
    returns: pygame.Surface
    """
    global cursor_texture, miss_texture, bg_texture, bg_surf, pg_surf, dark, mouse_visible
    pygame.init()

    pygame.mouse.set_visible(mouse_visible)
    if full_screen:
        try: 
            win = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        except Exception:
            print('Cannot set window, because resolution is too high.')
            logf.close()
            pygame.quit()
            quit()
    else:
        win = pygame.display.set_mode((width, height))

    
    cursor_texture = pygame.image.load('textures/cursor.png')
    cursor_texture = pygame.transform.scale(cursor_texture, (16, 16))

    miss_texture = pygame.image.load('textures/miss.png')
    miss_texture = pygame.transform.scale(cursor_texture, (16, 16))

    bg_textures = []
    i = 1
    while i <= 9:
        string = 'bg' + str(i)
        bg_textures.append(string)
        i += 1

    texture_no = bg_textures[random.randint(0, 8)]
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
        self.width = res[0]
        self.height = res[1]
        self.win = Initialize_window(self.width, self.height)
        self.is_running = True
        self.click_count = 0
        self.circles = []
        self.cursor_pos = (0, 0)
        self.playfield = {
        'topX': (self.width / 10),                      #top X
        'topY': (self.height / 10),                     #top Y
        'bottomX': (self.width - self.width / 10),      #bottom X
        'bottomY': (self.height - self.height / 10)}    #bottom Y
        self.points = 0
        self.combo = 0
        self.combo_color = color.white
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

        if self.CS < MIN_CS:
            self.CS = MIN_CS
        elif self.CS > MAX_CS:
            self.CS = MAX_CS

        if self.HP < MIN_HP:
            self.HP = MIN_HP
        elif self.HP > MAX_HP:
            self.HP = MAX_HP

    def Make_map(self, data):
        """
        rtype: array
        returns: array
        """
        global DEBUG_MODE
        global DEBUG_EXCEPTION
        lenght = len(data)
        ptr = 0

        circles = []
        for element in data:
            while ptr <= lenght-1:
                try:
                    posX = int(data[ptr])
                    posY = int(data[ptr+1])
                    time = int(data[ptr+2])

                    ptr += 3

                    obj = circle.Circle(self.win, posX, posY, time, g)
                    circles.append(obj)
                except IndexError:
                    if DEBUG_MODE:
                        DEBUG_EXCEPTION = "Program stopped incorrectly. Cannot make object, invalid map format."
                    else:
                        print("Cannot load map. Maybe map has outdated or invalid format.")
                
            return circles

    def Run(self):
        global DEBUG_MODE
        global DEBUG_EXCEPTION
        
        if not auto_generate:
            m = map.Map(DEBUG_MODE)
            map_data = m.Load_map('test')
            self.circles = self.Make_map(map_data)
            if type(self.circles).__name__ == 'str' or type(self.circles).__name__ == 'NoneType':
                DEBUG_EXCEPTION = self.circles
                if DEBUG_MODE:
                    print("Program stopped incorrectly. Stop cause: " + DEBUG_EXCEPTION)
                pygame.quit()
                quit()
        else:
            pass
        
        radius = stats.getCS(self.CS)

        while self.is_running:
            if auto_generate:
                if len(self.circles) <= 1:
                    obj = circle.Circle(self.win, random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomX'] - radius)), random.randint(int(self.playfield['topX'] + radius), int(self.playfield['bottomY'] - radius)), None , g)
                    self.circles.append(obj)

            start = time.perf_counter()
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.submit(self.Draw)
                executor.submit(self.HealthBar)
                executor.submit(self.Combo)
                executor.submit(self.Cursor)
                executor.submit(self.Time)
                executor.submit(self.Clicks)
                executor.submit(self.FPSCounter)

            self.events = pygame.event.get()

            if not self.circles:
                if DEBUG_MODE:
                    print("List depleted at: " + str(self.time))
                    DEBUG_EXCEPTION = "Objects list self.circles is empty."
                    
                    self.is_running = False

            for event in self.events: 
                self.cursor_pos = pygame.mouse.get_pos()               
                if event.type == pygame.QUIT:
                    if DEBUG_MODE:
                        DEBUG_EXCEPTION = "User interruption by closing window"
                    self.is_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if DEBUG_MODE:
                            DEBUG_EXCEPTION = "User interruption by closing window"
                        self.is_running = False

            if self.health <= 0:
                if DEBUG_MODE:
                    DEBUG_EXCEPTION = "self.health reached " + str(self.health)
                self.is_running = False

            pygame.display.update()

            clock.tick()
            finish = time.perf_counter()

            self.fps = int(clock.get_fps())
            self.render_time = round(finish - start, 3)
            self.time = pygame.time.get_ticks()

            if DEBUG_MODE and len(self.circles) < 10:
                print(self.circles)
            if DEBUG_MODE:
                print(len(self.circles))

        if DEBUG_MODE:
            print("Program stopped correctly. Stop cause: " + DEBUG_EXCEPTION)
        pygame.quit()
        quit()

    def Draw(self):
        global DEBUG_MODE
        global DEBUG_EXCEPTION

        self.win.blit(bg_texture, (0, 0))
        self.win.blit(dark, (0, 0))

        for circle in self.circles:
                if not auto_generate:
                    if self.time >= circle.time and self.time <= circle.time + stats.getAR(self.AR):
                        circle.Draw()
                        for event in self.events:
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_z or event.key == pygame.K_x:
                                    if circle.Collide():
                                        circle.Hit()
                                        self.circles.remove(circle)
                                    if not circle.Collide():
                                        self.circles.remove(circle)
                                        circle.Miss()

                                    self.click_count += 1
                    elif self.time >= circle.time + stats.getAR(self.AR):
                        self.circles.remove(circle)
                        circle.Miss()
                else:
                    circle.Draw()
                    for event in self.events:
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_z or event.key == pygame.K_x:
                                if circle.Collide():
                                    circle.Hit()
                                    self.circles.remove(circle)
                                if not circle.Collide():
                                    self.circles.remove(circle)
                                    circle.Miss()

                                self.click_count += 1

    def Cursor(self):
        self.win.blit(self.cursor_texture, (self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2))

    def Combo(self):
        font = pygame.font.SysFont("comicsansms", 48)
        text = 'points: ' + str(self.points)
        text_points = font.render(text, True, self.combo_color)
        text_combo = font.render('combo: ' + str(self.combo), True, color.white)
        lenght = len(text)

        self.win.blit(text_points, (self.width - lenght * 25, (self.height - 70)))
        self.win.blit(text_combo, (10, (self.height - 70)))

    def HealthBar(self):
        self.health -= stats.getHP(self.HP)

        if self.health > 100:
            self.health = 100

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

    def Time(self):
        font = pygame.font.SysFont("comicsansms", 24)
        time = round((self.time/1000), 2)
        text = font.render('Time: ' + str(time) + 's', True, color.white)
        pos = (self.width/10, 0)

        self.win.blit(text, pos)

    def Clicks(self):
        font = pygame.font.SysFont("comicsansms", 24)
        pos = ((self.width - (24*1.5)), (self.height/2))
        text = font.render(str(self.click_count), True, color.white)

        self.win.blit(text, pos)

    def FPSCounter(self):
        font = pygame.font.SysFont("comicsansms", 12)
        string = 'Render time: ' + str(self.render_time) + 's | FPS: ' + str(self.fps)
        text = font.render(string, True, color.white)
        pos = (self.playfield['topX'] + len(string) * 12, self.playfield['bottomY'] - 24)

        self.win.blit(text, pos)

class Interface():
    time = None
    clicks = None
    fps = None
    health = None
    combo = None

    font = None

    def __init__(self, game):
        self.g = game

    def setFont(size):
        """
        rtype: int
        returns: None
        """
        font = pygame.font.SysFont('comicsansms', size)
        Interface.font = font

    def setText(text, color):
        """
        rtype: str, tuple(3xE)
        returns: None
        """
        return Interface.font.render(text, True, color)

    def FPSCounter():
        pass

    def Draw(win, *args):
        """
        rtype: pygame.Surface, function
        """
        for e in args:
            win.blit(e)


if __name__ == '__main__':
    try:
        update.Check_version()
        
        g = Game(resolution)

        g.Run()
    except Exception:
        with open('log.txt', 'w+') as logf:
            logf.write(traceback.format_exc())
            print(traceback.format_exc())
        pygame.quit()
        quit()

        os.system('pause >NUL')
    
#finish making clicks display and make background for it
#add miss animation (use image.alpha operations)
#improve performance/make more Surfaces
#move combo, health and whole interface to different class
