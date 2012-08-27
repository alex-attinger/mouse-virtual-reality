'''
Created on Aug 20, 2012

@author: alexattinger_3
'''

class Camera(object):
    '''
    classdocs
    '''


    def __init__(self,origin,focus,up):
        '''
        Constructor
        '''
        self.origin=Point(-10,-10,5)
        self.focus=Point(0,0,0)
        self.up=Point(0,0,1)
        
        self.focalLength=50
        self.aperture=90
        self.origin.x=origin.x
        self.origin.y=origin.y
        self.origin.z=origin.z
        self.focus.x=focus.x
        self.focus.y=focus.y
        self.focus.z=focus.z
        
        self.up.x=up.x
        self.up.y=up.y
        self.up.z=up.z
        

class Point(object):
    
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.z=z