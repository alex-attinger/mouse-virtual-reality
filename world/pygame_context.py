import pygame
import sys

from OpenGL.GL import *
from numpy import sin, cos, pi

class MyContext():
    def  __init__(self):
        pygame.init()
        self._createScreen()
        
        return
        
    def flip(self):
        pygame.display.flip()
        return
        
    def render(self):
        self.angle=60
        self.res=1
        self.r_in = .55
        self.r_out = 4
     
        pass
        
    def _createScreen(self):
        '''
        Create pygame screen using SCREEN_RESOLUTION and FULLSCREEN parameters
        '''
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL
      
        self.screen = pygame.display.set_mode((512, 512), flags)
        self.clock = pygame.time.Clock()
        
    def run(self):
        running = True
        while running:
            self.render()
            self.flip()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
        return

if __name__ == '__main__':
    app=MyContext()
    app.run()
    sys.exit(1)
