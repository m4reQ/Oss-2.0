import pygame
import game

class Menu():
        def __init__(self, g):
                self.win = g.win
                self.height = g.height
                self.width = g.width
                self.is_running = True
                self.select_mode = None
                self.map = None
                self.cursor_texture = g.cursor_texture
                self.cursor_pos = (0, 0)
                self.start = False
                
        
        def Title(self):
                pass
        
        def Mode(self):
                pass
        
        def Map_Select(self):
                pass

        def Stats(self):
                #temporary
                pass

        def Cursor(self):
                self.cursor_pos = pygame.mouse.get_pos()
        
                self.win.blit(self.cursor_texture, (self.cursor_pos[0] - self.cursor_texture.get_width()/2, self.cursor_pos[1] - self.cursor_texture.get_height()/2))
        
        def Draw(self):
                self.win.blit(game.bg_texture, (0, 0))
                self.Cursor()

        def Run(self):
                while self.is_running:
                        self.Draw()
                        pygame.display.update()

        def Start(self):
                self.start = True
                self.is_running = False

if __name__ == "__main__":
        pygame.quit()
        quit()
