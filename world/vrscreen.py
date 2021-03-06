from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from numpy import sin, cos, pi
from VR.world.pygame_context import MyContext
import sys

class VRScreen():
    
    pass
    
class VRScreenElement():
    '''Create single Elements for the vr screen'''
    
    def __init__(self, angle=60, res=1, r_in=.55, r_out=3, starting_angle = 0):
        '''
        Initialize a single Element for the vr screen
        angle: the angular 'width' of the element (i.e. 360/nElements)
        res: how many quads per degree
        r_in/r_out:  inner/outer radius of screen
        '''
        self.angle = angle
        self.res = res
        self.r_in = r_in
        self.r_out = r_out
        self.starting_angle = starting_angle
        return

    def render(self):
        #glLoadIdentity()
        glColor4f(1.0, 1.0, 1.0, 1.0)
        glutSolidSphere(.55,40,20)
        nquads=int(self.angle*self.res)
        delta_tex = 1.0/nquads
        delta_alpha=self.angle*1.0*pi/(nquads*180)
        glBegin(GL_QUAD_STRIP)
        alpha=0
        print delta_alpha
        div = 100
        for i in range(nquads+1):
#            al=pi/2-i*delta_alpha
#            glVertex(self.r_out*cos(al), self.r_out*sin(al), 0)
#            glVertex(self.r_in*cos(al), self.r_in*sin(al), 0)
            alpha=pi/2.0-i*delta_alpha-self.starting_angle
    
            glTexCoord2f(i*delta_tex,0)
            glVertex3f(self.r_out*cos(alpha), self.r_out*sin(alpha), 0.0)
            glTexCoord2f(i*delta_tex, 1)
            glVertex3f(self.r_in*cos(alpha), self.r_in*sin(alpha), 0.0)
        glEnd()
        pass
        
class Debug(MyContext):
    def __init__(self):
        MyContext.__init__(self)
        self.elements = []
        n=6
        for i in range(n):
            self.elements.append(VRScreenElement(r_in=.55, angle=360/n, res=.5, starting_angle = i*2*pi/n))
        
        glClearColor(0.0, 0.0, 0.0, 0.0)
        
        glMatrixMode(GL_PROJECTION)
        gluPerspective(70.,1.,1.,40.)
    
        glMatrixMode(GL_MODELVIEW)
        gluLookAt(0,0,10,
              0,0,0,
              0,1,0)
        glPolygonMode(GL_FRONT_AND_BACK,GL_LINE);
        return
    def render(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for e in self.elements:
            e.render()
        
        self.flip()
        return
        
        
if __name__== '__main__':
    app=Debug()
    app.run()
    sys.exit()
    
