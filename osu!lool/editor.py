try:
	import pygame
	import os
	import traceback
	from game import width, height
	from helper import color
except Exception:
	logf = open('log.txt', 'w+')
	logf.write(traceback.format_exc())
	logf.close()

	os.system('pause >NUL')
	pygame.quit()
	quit()

#debug mode
DEBUG_MODE = True
DEBUG_EXCEPTION = ''

#mouse visibility
mouse_visible = False

#cursor texture
cursor_texture = None

#register mode
reg_mode = 'p'

#save files
timef = open(os.path.join('maps', 'time.txt'), 'w+')
posf = open(os.path.join('maps','position.txt'), 'w+')

def Initialize_window(width, height):
	"""
    rtype: int, int
    returns: pygame.Surface
    """
	global cursor_texture
	pygame.init()

	pygame.mouse.set_visible(mouse_visible)

	win = pygame.display.set_mode((width, height))
	cursor_texture = pygame.image.load('textures/cursor.png')
	cursor_texture = pygame.transform.scale(cursor_texture, (16, 16))

	return win

class Editor():
	def __init__(self, width, height):
		self.width = width
		self.height = height
		self.win = Initialize_window(self.width, self.height)
		self.is_running = True
		self.playfield = {
		'topX': (self.width / 10),                      #top X
		'topY': (self.height / 10),                     #top Y
		'bottomX': (self.width - self.width / 10),      #bottom X
		'bottomY': (self.height - self.height / 10)}    #bottom Y
		self.cursor_texture = cursor_texture
		self.cursor_pos = (0, 0)
		self.time = 0
		self.last_regs = [(0, 0), (0, 0)]

	def Run(self):
		global i
		dark = pygame.Surface((width, height))
		dark.fill((0, 0, 0))
		i = 0
		while self.is_running:
			self.win.blit(dark, (0, 0))
			self.Time()
			self.Point(color.red, self.last_regs[0])
			self.Point(color.green, self.last_regs[1])
			self.Cursor()

			events = pygame.event.get()
			for event in events:
				self.cursor_pos = pygame.mouse.get_pos()
				if event.type == pygame.QUIT:
					self.is_running = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_z or event.key == pygame.K_x:
						if self.cursor_pos[0] > self.playfield['topX'] and self.cursor_pos[0] < self.playfield['bottomX']:
							if self.cursor_pos[1] > self.playfield['topY'] and self.cursor_pos[1] < self.playfield['bottomY']:
								self.Click()

			pygame.display.update()
			self.time = pygame.time.get_ticks()

		pygame.quit()
		quit()

	def Cursor(self):
		self.win.blit(self.cursor_texture, (self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2))

	def Click(self):
		global reg_mode, i
		if DEBUG_MODE:
			print('Last registered: ' + str(self.time) + ', ' + str(self.cursor_pos))

		if reg_mode == 't':
			timef.write(str(i) + '. Object at time: ' + str(self.time) + '\n')

			i += 1
		elif reg_mode == 'p':
			posf.write(str(i) + '. Object at position: ' + str(self.cursor_pos) + '\n')
			last_reg = self.cursor_pos

			self.last_regs[0] = self.last_regs[1]
			self.last_regs[1] = last_reg

			i += 1
		else:
			print('Wrong register mode! Changing register mode to "time".')
			reg_mode = 't'

	def Time(self):
		font = pygame.font.SysFont("comicsansms", 24)
		text = font.render('Time: ' + str(self.time) + 'ms', True, color.white)
		pos = (0, 0)

		self.win.blit(text, pos)

	def Point(self, color, pos):
		pygame.draw.circle(self.win, color, pos, 2)

if __name__ == '__main__':
	e = Editor(width, height)

	clock = pygame.time.Clock()
	clock.tick(1000)

	e.Run()