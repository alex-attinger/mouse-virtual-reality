'''
Created on Aug 20, 2012

@author: alexattinger_3
'''

import numpy
import sys

class Camera(object):
    '''
    datastructure to hold information about a camera
    '''


    def __init__(self,origin,focus,aperture=None,  up=None):
        '''
        Constructor
        '''
        self.origin=Point(-10,-10,5)
        self.focus=Point(0,0,0)
        self.up=Point(0,0,1)
        
        self.focalLength=50
        self.aperture=aperture
        self.origin.x=origin.x
        self.origin.y=origin.y
        self.origin.z=origin.z
        self.focus.x=focus.x
        self.focus.y=focus.y
        self.focus.z=focus.z
        if up:
            self.up.x=up.x
            self.up.y=up.y
            self.up.z=up.z
        else:
            #lleave up as it was
            pass
        return
        
    

class Point(object):
    
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z
        return

    def length(self):
        return numpy.sqrt(self.x**2, self+y**2+self.z**2)
    
    def length2D(self):
        return numpy.sqrt(self.x**2 +  self.y**2)
        
    def heading_angle(self):
        '''
        return the heading angle in radians screen coordinate system in the x-y plane
        0 if point lies on positive y - axis, clockwise : positive
        '''
        if self.x==0 and self.y == 0:
            return  0
        elif self.x>=0:
            return numpy.arccos(self.y/self.length2D())
        else:
            return -numpy.arccos(self.y/self.length2D())
        return 0

if __name__=='__main__':
    p1 = Point(0, 0, 0)
    print len(sys.argv)
