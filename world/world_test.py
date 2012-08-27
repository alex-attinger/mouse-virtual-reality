'''
Created on Aug 16, 2012

@author: alexattinger_3
'''
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import sin, cos, pi 

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.camx=-10
        self.camy=-10
        self.camz=5
        self.delta_step=.1
        self.delta_angle=.01*pi
        
        self.headingDir=[1,0]
        self.angle=pi/4
        self.length=10
        
        self.lookAt_X=0
        self.lookAt_Y=0
        self.lookAt_Z=2
        self.updateHeading()
        self.updateLookPos()
        
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(850,850)
        glutInitWindowPosition(310,30)
        glutCreateWindow('world')
    
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
        glutDisplayFunc(self.display)
        #glutIdleFunc(move)
        #glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special_keyboard)
        
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70.,1.,1.,100.)
        
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(self.camx,self.camy,self.camz,
                  self.lookAt_X,self.lookAt_Y,self.lookAt_Z,
                  0,0,1)
        
        
        glutMainLoop()
        
        return
    
    def display(self):
        glLoadIdentity()
        gluLookAt(self.camx,self.camy,self.camz,
                   self.lookAt_X,self.lookAt_Y,self.lookAt_Z,
                 0,0,1)
        print('x %d, y %d z %d'%(self.camx,self.camy,self.camz))
        print('lx %f, y %f, z %f'%(self.lookAt_X,self.lookAt_Y,self.lookAt_Z))
        
        
        glMatrixMode(GL_MODELVIEW)
        
        #glLoadIdentity()
        black=[0.0,0.0,0.0,0.0]
        white=[1.0,1.0,1.0,1.0]
        red=[1.0,0,0,1]
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        #floor
        glColor4fv(white)
        glBegin(GL_QUADS)
        glVertex3f(-100,-100,0)
        glVertex3f(100,-100,0)
        glVertex3f(100,100,0)
        glVertex3f(-100,100,0)
        glEnd()
        glPopMatrix()
        
        glColor4fv(black)
        glBegin(GL_LINES)
        for i in range(200):
            glVertex3f(-100+i,-100,0)
            glVertex3f(-100+i,100,0)
        glEnd()
        
        glPushMatrix()
        glTranslate(50,50,3)
        glColor4fv(red)
        glutSolidSphere(3,40,20)
        glPopMatrix()
        
        glPushMatrix()
        glColor4fv(red)
        glTranslatef(30,0,10)
        glutSolidSphere(10,40,20)
        glPopMatrix()
        
        glPushMatrix()
        glTranslatef(0,0,5)
        glColor4fv(red)
        glutWireCube(5)
        glPopMatrix()
        
        glutSwapBuffers()
        
    
        return
    def updateLookPos(self):
        '''
        update Position of Camera eye point, call this function whenever camera position changed,
        use updateHeading when orientation changed
        '''
        self.lookAt_X=self.camx+self.headingDir[0]*self.length
        self.lookAt_Y=self.camy+self.headingDir[1]*self.length
        return
        
    def updateHeading(self):
        '''
        update Position after rotation of camera
        '''
        self.headingDir[0]=cos(self.angle)
        self.headingDir[1]=sin(self.angle)
        self.updateLookPos()
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
    print 'here'
    app=MyClass()