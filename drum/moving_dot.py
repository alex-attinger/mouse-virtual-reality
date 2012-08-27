'''
Created on Aug 16, 2012

@author: alexattinger_3
'''
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import sys
import time
from math import sin, cos

import pygame

name = 'ball_glut'
dx=0.0
dy=0.0
xPos=0.0
yPos=0.0
orbit=1.1
ti=0
t0=0
freq=1
def main():
    #glutInit(sys.argv
    
#    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
#    glutInitWindowSize(850,850)
#    glutInitWindowPosition(310,30)
#    glutCreateWindow(name)
    pygame.init()
    create_screen()
    glClearColor(0.,0.,0.,1.)

#    glutDisplayFunc(display)
#    glutIdleFunc(move)
#    glutKeyboardFunc(keyboard)
    
    glMatrixMode(GL_PROJECTION)
    gluPerspective(40.,1.,1.,40.)
    
    glMatrixMode(GL_MODELVIEW)
    gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
    
    t0=time.time()
    run()

    return
def create_screen():
        '''
        Create pygame screen using SCREEN_RESOLUTION and FULLSCREEN parameters
        '''
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL
      
        screen = pygame.display.set_mode((512, 512), flags)
        clock = pygame.time.Clock()

def display():
    black=[0.0,0.0,0.0,0.0]
    white=[1.0,1.0,1.0,1.0]
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
  
    glColor4fv(white)
    glutSolidSphere(3,40,20)
    glColor4fv(black)
    glutSolidSphere(.45,40,20)
    
    
    
    glPopMatrix()
    glPushMatrix()
    glTranslatef(orbit*sin(freq*ti),orbit*cos(freq*ti),0)
    glColor4fv(black)
    glutSolidSphere(.02,20,20)
    glPopMatrix()
    #glutSwapBuffers()
    pygame.display.flip()
    
    return
    
def run():
    running = True
    while running:
        move()
        display()
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                      
    #pygame.display.quit()
    return

def move():
    #t=time.clock()
    global ti, t0
    ti=time.time()-t0
    #glutPostRedisplay()

def keyboard(key,x,y):
    global freq,orbit
    if key =='+':
        freq=freq+0.3
    elif key == '-':
        freq = freq -0.3
    elif key == 'i':
        orbit = orbit -.1
    elif key == 'o':
        orbit = orbit + .1
    

if __name__ == '__main__': main()
sys.exit()
