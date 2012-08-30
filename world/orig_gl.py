'''
Created on Aug 20, 2012

@author: alexattinger_3
'''
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from numpy import sin, cos, pi, sqrt
from VR.world.camera import Camera, Point
import sys



class MyClass(object):
    '''
    classdocs
    '''
    

    def __init__(self):
        '''
        Constructor
        '''
        self.screenwidth = 800
        self.screenheight = 800
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        glutInitWindowSize(self.screenwidth,self.screenheight)
        glutInitWindowPosition(310,30)
        glutCreateWindow('world')
        
    
        #self.setupParams()
        if len(sys.argv) >= 1:
            if sys.argv[1] == '0':
                glutDisplayFunc(self.display)
            elif sys.argv[1] == '1':
                glutDisplayFunc(self.debug)
            elif sys.argv[1] == '2':
                glutDisplayFunc(self.drawSceneView)
            else:
                glutDisplayFunc(self.display)
        else:
            glutDisplayFunc(self.display)
        
       
        #special functions
        glutKeyboardFunc(self.keyboard)
        glutSpecialFunc(self.special_keyboard)
        #the camera that whill watch the textures:
        self.homeCam=Camera(Point(0,0,10),Point(0,0,0),up=Point(0,1,0), aperture = 90)
        #the cameras used to generate textures
        self.nCams = 8
        self.heading = 0
        self.currentPos = Point(0, 0, 0)
        self.camList = self._generateCameras(self.nCams, self.currentPos, heading=self.heading)
        for c in self.camList:
            print str(c.focus.x) + '\t' + str(c.focus.y)

        glutMainLoop()
   
        return
    
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
        
    def _generateCameras(self, nCams, position, heading=0):
        '''
        generate a list of n camera objects at position, the cameras together will cover 360,
        list is clockwise arangement of cameras,
        heading defines the angular deviation of the first camera in radians relative to y axis. Clockwise is positive
        
        '''
        aperture = 360.0/nCams
        
        delta_alpha=2*pi/nCams
        length = 10
        angle_offset = heading
        
        camlist=[]
        for i in range(nCams):
            alpha = pi/2 - i*delta_alpha+angle_offset
            current_look_at = Point(position.x+length*cos(alpha), position.y+length*sin(alpha), 4)
            camlist.append(Camera(position,current_look_at, aperture = aperture ))
            
        
        
        return camlist
        
    def drawSceneView(self):
        glLoadIdentity()
        #holding pixel data
        texture=[]
        #generate texture names
        textureid=[]
        textureid=glGenTextures(self.nCams)
        #glMatrixMode(GL_PROJECTION);
        #make a texcam
        #gluPerspective(360.0/self.nCams,1.,1.,100.)
    
       
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90,1.,1.,100.)
    
        glMatrixMode(GL_MODELVIEW);
        gluLookAt(0, 0, 20,
                  0, 0, 0,
                  0, 1, 0)
     

        glDrawBuffer(GL_BACK);
        glClearColor(0.0,0.0,0.0,0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        self.drawScene()
        #draw Camera representation a line goes from origin/eyepoint to the look_at position
        
        glBegin(GL_LINES)
        for i in range(self.nCams):
            currentCam = self.camList[i]
            glVertex3f(currentCam.origin.x, currentCam.origin.y, currentCam.origin.z)
            glVertex3f(currentCam.focus.x, currentCam.focus.y, currentCam.focus.z)
        glEnd()
        
        #force empty buffer
        glFlush();

        glutSwapBuffers()
        
        return
    
        
    def debug(self):
        glLoadIdentity()
        #holding pixel data
        texture=[]
        #generate texture names
        textureid=[]
        textureid=glGenTextures(self.nCams)
        #glMatrixMode(GL_PROJECTION);
        #make a texcam
        #gluPerspective(360.0/self.nCams,1.,1.,100.)
        for i in range(self.nCams):
            currentCam = self.camList[i]
            print str(currentCam.focus.x) +'\t' +str(currentCam.focus.y)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(360.0/self.nCams,1.,1.,100.)
        
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(currentCam.origin.x,currentCam.origin.y,currentCam.origin.z,
                       currentCam.focus.x,currentCam.focus.y,currentCam.focus.z,
                     currentCam.up.x,currentCam.up.y,currentCam.up.z)
         
 
            glDrawBuffer(GL_BACK);
            glClearColor(0.0,0.0,0.0,0.0);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            self.drawScene()
            
            
            #force empty buffer
            glFlush();
        
            #read the pixel data from framebuffer
            texture.append(glReadPixels(0,0,self.screenwidth,self.screenheight,GL_RGBA,GL_UNSIGNED_BYTE))
            
            glBindTexture(GL_TEXTURE_2D,textureid[i])
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D,0,4,
                            self.screenwidth,self.screenheight,
                            0,GL_RGBA,GL_UNSIGNED_BYTE,texture[i])
            glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL);
                     
        
#        #Now everything is set up to draw 'real screen'
        glDrawBuffer(GL_BACK);
        glClearColor(0.5,0.5,1.0,0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLineWidth(1.0);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(self.homeCam.aperture, 1.0,0.1,1000.0);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        #look from top at tile
        gluLookAt(self.homeCam.origin.x,self.homeCam.origin.y,self.homeCam.origin.z,
                   self.homeCam.focus.x,self.homeCam.focus.y,self.homeCam.focus.z,
                    self.homeCam.up.x,self.homeCam.up.y,self.homeCam.up.z);
        
        glDisable(GL_LIGHTING);
        glShadeModel(GL_FLAT);
        #glLightModelfv(GL_LIGHT_MODEL_AMBIENT,white);
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        #DrawTile
        for i in range(self.nCams):
            glEnable(GL_TEXTURE_2D);
            glBindTexture(GL_TEXTURE_2D,textureid[i])
            glColor3f(.9,.9,.9)
            
            
            self._renderScreenElement(offset_rad = -pi/self.nCams+i*2*pi/self.nCams, angle_rad = 2*pi/self.nCams, res=1)
            
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_DEPTH_TEST)
        glutSwapBuffers()
        glDeleteTextures(textureid)
        
        return
    
    def display(self):
        glLoadIdentity()
        #holding pixel data
        texture=[]
        #generate texture names
        textureid=[]
        textureid=glGenTextures(self.nCams)
        #glMatrixMode(GL_PROJECTION);
        #make a texcam
        #gluPerspective(360.0/self.nCams,1.,1.,100.)
        for i in range(self.nCams):
            currentCam = self.camList[i]
            print str(currentCam.focus.x) +'\t' +str(currentCam.focus.y)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(360.0/self.nCams,1.,1.,100.)
        
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(currentCam.origin.x,currentCam.origin.y,currentCam.origin.z,
                       currentCam.focus.x,currentCam.focus.y,currentCam.focus.z,
                     currentCam.up.x,currentCam.up.y,currentCam.up.z)
         
 
            glDrawBuffer(GL_BACK);
            glClearColor(0.0,0.0,0.0,0.0);
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
            self.drawScene()
            
            
            #force empty buffer
            glFlush();
        
            #read the pixel data from framebuffer
            texture.append(glReadPixels(0,0,self.screenwidth,self.screenheight,GL_RGBA,GL_UNSIGNED_BYTE))
            
            glBindTexture(GL_TEXTURE_2D,textureid[i])
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_S,GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D,GL_TEXTURE_WRAP_T,GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D,0,4,
                            self.screenwidth,self.screenheight,
                            0,GL_RGBA,GL_UNSIGNED_BYTE,texture[i])
            glTexEnvf(GL_TEXTURE_ENV,GL_TEXTURE_ENV_MODE,GL_DECAL);
                     
        
#        #Now everything is set up to draw 'real screen'
        glDrawBuffer(GL_BACK);
        glClearColor(0.5,0.5,1.0,0.0);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
        glLineWidth(1.0);
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        gluPerspective(self.homeCam.aperture, 1.0,0.1,1000.0);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        #look from top at tile
        gluLookAt(self.homeCam.origin.x,self.homeCam.origin.y,self.homeCam.origin.z,
                   self.homeCam.focus.x,self.homeCam.focus.y,self.homeCam.focus.z,
                    self.homeCam.up.x,self.homeCam.up.y,self.homeCam.up.z);
        
        glDisable(GL_LIGHTING);
        glShadeModel(GL_FLAT);
        #glLightModelfv(GL_LIGHT_MODEL_AMBIENT,white);
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
        #glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
        #DrawTile
        for i in range(self.nCams):
            glEnable(GL_TEXTURE_2D);
            glBindTexture(GL_TEXTURE_2D,textureid[i])
            glColor3f(.9,.9,.9)
            
            
            self._renderScreenElement(offset_rad = -pi/self.nCams+i*2*pi/self.nCams, angle_rad = 2*pi/self.nCams, res=1)
            
            glDisable(GL_TEXTURE_2D)
            glEnable(GL_DEPTH_TEST)
        glutSwapBuffers()
        glDeleteTextures(textureid)
        
        return
    
    def _renderScreenElement(self, r_in=.55, r_out=4, res=1, offset_rad=0, angle_rad=pi/3):
        '''
        generate a Screen Element
        inner radius, outer radius, resolution (quad per deg), angle in radians
        '''
        
        nquads=int(angle_rad*res/pi*180)
        delta_tex = 1.0/nquads
        delta_alpha=angle_rad/nquads
        glBegin(GL_QUAD_STRIP)
        alpha=0
        
        div = 100
        for i in range(nquads+1):
            alpha=pi/2.0-i*delta_alpha-offset_rad
    
            glTexCoord2f(i*delta_tex,0)
            glVertex3f(r_out*cos(alpha), r_out*sin(alpha), 0.0)
            glTexCoord2f(i*delta_tex, 1)
            glVertex3f(r_in*cos(alpha), r_in*sin(alpha), 0.0)
        glEnd()

    def keyboard(self, key, x, y):
        
        if key=='r':
            #rotate
            self.heading = self.heading + pi/10
            self.camList = self._generateCameras(self.nCams, self.currentPos, heading=self.heading)
            glutPostRedisplay()
        elif key == 'w':
            #move forward
            stepsize = 1
            self.currentPos.x += sin(self.heading)*stepsize
            self.currentPos.y += cos(self.heading)*stepsize
            self.currentPos.z += self.currentPos.z
            self.camList = self._generateCameras(self.nCams, self.currentPos, heading=self.heading)
            glutPostRedisplay()
            
        return
    def special_keyboard(self,key,x,y):
        
        pass
        return
    
    def drawScene(self):
        glPolygonMode(GL_FRONT_AND_BACK,GL_FILL);
        black=[0.0,0.0,0.0,1.0]
        white=[1.0,1.0,1.0,1.0]
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
        
        #cubes
        glPushMatrix()
        glTranslate(0,10,0)
        glColor4f(0.0, 1.0, 1.0, 1.0)
        glutSolidCube(5)
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(10,0,0)
        glColor4f(1.0, 0.0, 0.0, 1.0)
        glutSolidCube(2)
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(0,-10,0)
        glColor4f(.0, 1.0, 0.0, 1.0)
        glutSolidCube(2)
        glPopMatrix()
        
        glPushMatrix()
        glTranslate(-10,0,0)
        glColor4f(0.0, 0.0, 1.0, 1.0)
        glutSolidCube(2)
        glPopMatrix()
        return
        
    
    
if __name__=='__main__':
    
    app=MyClass()
