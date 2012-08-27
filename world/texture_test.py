'''
Created on Aug 20, 2012

@author: alexattinger_3
'''
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import sin, cos, pi 
from world.camera import Camera, Point

import pygame


class MyClass(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        

#        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
#        glutInitWindowSize(512,512)
#        glutInitWindowPosition(310,30)
#        glutCreateWindow('world')
        self.create_screen()
    
        #self.setupParams()
        
        #glutDisplayFunc(self.display)
        #glutIdleFunc(move)
        #glutKeyboardFunc(self.keyboard)
        #glutSpecialFunc(self.special_keyboard)
        #the camera that whill watch the textures:
        self.homeCam=Camera(Point(0,0,10),Point(0,0,0),Point(0,1,0))
        
        #glutMainLoop()

        return
        
    def create_screen(self):
        '''
        Create pygame screen using SCREEN_RESOLUTION and FULLSCREEN parameters
        '''
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE | pygame.OPENGL
      
        self.screen = pygame.display.set_mode((512, 512), flags)
        self.clock = pygame.time.Clock()
    
    def setupParams(self):
        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LINE_SMOOTH)
        glDisable(GL_POINT_SMOOTH)
        glDisable(GL_POLYGON_SMOOTH) 
        glDisable(GL_DITHER)
        glDisable(GL_CULL_FACE)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA,GL_ONE_MINUS_SRC_ALPHA)
        glLineWidth(1.0)
        glPointSize(1.0)
        glFrontFace(GL_CW)
        glClearColor(0.0,0.0,0.0,0.0)
        glColorMaterial(GL_FRONT_AND_BACK,GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        return
    
    def display(self):
        glLoadIdentity()
        #holding pixel data
        texture=[]
        #generate texture names
        textureid=[]
        textureid=glGenTextures(1);
        #glMatrixMode(GL_PROJECTION);
        #make a texcam
       
        tcam=Camera(Point(-10,-10,5),Point(0,0,2),Point(0,0,1))
        gluPerspective(70.,1.,1.,100.)
        
        glMatrixMode(GL_MODELVIEW);
        gluLookAt(tcam.origin.x,tcam.origin.y,tcam.origin.z,
                   tcam.focus.x,tcam.focus.y,tcam.focus.z,
                 tcam.up.x,tcam.up.y,tcam.up.z)
     
 
        glDrawBuffer(GL_BACK);
        glClearColor(0.0,0.0,0.0,0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        
       

        
        
        
        
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
        
       
        black=[0.0,0.0,0.0,0.0]
        white=[1.0,1,1,1.0]
        red=[1.0,0,0,1]
        
        glPushMatrix()
        
        #Draw some stuff
        #floor
        glColor4fv(white)
        glBegin(GL_QUADS)
        glVertex3f(-100,-100,0)
        glVertex3f(100,-100,0)
        glVertex3f(100,100,0)
        glVertex3f(-100,100,0)
        glEnd()
        glPopMatrix()
        
#        glColor4fv(black)
#        glBegin(GL_LINES)
#        for i in range(400):
#            glVertex3f(-100+i*.5,-100,0)
#            glVertex3f(-100+i*.5,100,0)
#        glEnd()
        #a sphere
        glPushMatrix()
        glTranslate(50,50,3)
        glColor4fv(red)
        glutSolidSphere(3,40,20)
        glPopMatrix()
        #another sphere
        glPushMatrix()
        glColor4fv(red)
        glTranslatef(30,0,10)
        glutSolidSphere(10,40,20)
        glPopMatrix()
        #a wire cube
        glPushMatrix()
        glTranslatef(0,0,5)
        glColor4fv(red)
        glutWireCube(5)
        glPopMatrix()
        #force empty buffer
        glFlush();
        
        #read the pixel data from framebuffer
        texture=glReadPixels(0,0,512,512,
         GL_RGBA,GL_UNSIGNED_BYTE);
        
        glBindTexture(GL_TEXTURE_2D,textureid)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D,0,4,
                        512,512,
                        0,GL_RGBA,GL_UNSIGNED_BYTE,texture)
        glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL);
                     
        
#        #Now everything is set up to draw 'real screen'
        glDrawBuffer(GL_BACK);
        glClearColor(0.5,0.5,1.0,0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLineWidth(1.0);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(self.homeCam.aperture,1.0,0.1,1000.0);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        #look from top at tile
        gluLookAt(self.homeCam.origin.x,self.homeCam.origin.y,self.homeCam.origin.z,
                   self.homeCam.focus.x,self.homeCam.focus.y,self.homeCam.focus.z,
                    self.homeCam.up.x,self.homeCam.up.y,self.homeCam.up.y);
        
        glDisable(GL_LIGHTING);
        glShadeModel(GL_FLAT);
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT,white);
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
        
        #DrawTile
        glEnable(GL_TEXTURE_2D);
        glBindTexture(GL_TEXTURE_2D,textureid)
        glColor3f(1.0,1.0,1.0)
        
        glBegin(GL_QUADS)
        glTexCoord2f(0,0)
        glVertex3f(-5,-5,0)
        glTexCoord2f(1.0,0.0)
        glVertex3f(5,-5.0,0)
        glTexCoord2f(1.0,1.0)
        glVertex3f(3.0,5.0,0)
        glTexCoord2f(0.0,1.0)
        glVertex3f(-3
                   ,5.0,0)
        
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_DEPTH_TEST)
        
        #glutSwapBuffers()
        pygame.display-flip()
        glDeleteTextures(textureid)
        
        return
    
    def run(self):
        while True:
            self.display()
        return
    
    def special_keyboard(self,key,x,y):
        
        if key == GLUT_KEY_LEFT:
            self.angle += self.delta_angle
            self.updateHeading()
            glutPostRedisplay()
            return
           
        elif key == GLUT_KEY_RIGHT:
            self.angle -=self.delta_angle
            self.updateHeading()
            glutPostRedisplay()
            return
        elif key == GLUT_KEY_UP:
            self.camx += self.headingDir[0]*self.delta_step
            self.camy += self.headingDir[1]*self.delta_step
            self.updateLookPos()

            glutPostRedisplay()
            return
        elif key == GLUT_KEY_DOWN:
            self.camx -= self.headingDir[0]*self.delta_step
            self.camy -= self.headingDir[1]*self.delta_step
            self.updateLookPos()

            glutPostRedisplay()
        else:
            pass
    
        return
    

        
    
    
if __name__=='__main__':
    
    app=MyClass()
    app.run()
