'''
Created on Aug 15, 2012

@author: alexattinger_3
'''

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time
from math import sin, cos, pi
import pygame


name = 'ball_glut'
dx=0.0
dy=0.0
xPos=0.0
yPos=0.0
orbit=1.5
ti=0
t0=0
freq=1
def main():
    pygame.init()
    create_screen()

    glClearColor(0.,0.,0.,1.)
    ## glShadeModel(GL_SMOOTH)
    ## glEnable(GL_CULL_FACE)
    ## glEnable(GL_DEPTH_TEST)
    ## glEnable(GL_LIGHTING)
    ## lightZeroPosition = [10.,4.,10.,1.]
    ## lightZeroColor = [.5,1.0,1.,1.0] #green tinged
    ##                                   #glLightfv(GL_LIGHT0, GL_SPECULAR, lightZeroPosition)
    ##                                   #glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    ## glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
    ## glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    ## glLightfv(GL_LIGHT0,GL_AMBIENT,lightZeroColor)
    #glEnable(GL_LIGHT0)
   
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    ## gluLookAt(10,0,0,
    ##           0,0,0,
    ##           0,0,1)
    ## glPushMatrix()
    
    t0=time.time()
    
    run()
    sys.exit(1)
    return
    
def run():
    running = True
    while running:
        display()
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                      
    #pygame.display.quit()
    return


def display():
    black=[0.0,0.0,0.0,0.0]
    white=[1.0,1.0,1.0,1.0]
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    
    glColor4f(1.0,0.5,.9,1)
    seg=360
    height = 10
    radius=.55
    glBegin(GL_QUADS)
    for i in range(seg):
        c=.5*sin(i*12.0/180*pi)+0.5
        glColor4f(c,c,c,1)
       
        glVertex3f(radius*cos(i*pi*2.0/seg),radius*sin(i*pi*2.0/seg),0)
        glVertex3f(radius*cos((i+1)*pi*2.0/seg),radius*sin((i+1)*pi*2.0/seg),0)
        glVertex3f(radius*cos((i+1)*pi*2.0/seg),radius*sin((i+1)*pi*2.0/seg),height)
        glVertex3f(radius*cos(i*pi*2.0/seg),radius*sin(i*pi*2.0/seg),height)
        
    glEnd()

  
    glColor4fv(black)
    glutSolidSphere(.55,40,20)
    
    
    

    
    pygame.display.flip()
    
    return
    
def create_screen():
        '''
        Create pygame screen using SCREEN_RESOLUTION and FULLSCREEN parameters
        '''
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL
      
        screen = pygame.display.set_mode((900, 900), flags)
        clock = pygame.time.Clock()






if __name__ == '__main__': main()
