from PyQt4 import QtCore
import socket
import sys

class MouseReader(QtCore.QThread):
    
    '''
    This class reads bytes from /dev/input/mouse0
    works only on linux and needs superuser privileges to access dev/input/mouse0
    usage: MyObj = MouseReader()
    MyObj.start()
    MyObj.get... to get data
    
    '''
    

    def __init__(self, recorder = False, dev='/dev/input/mouse0'):
        
        if not sys.platform.startswith('linux'):
            print 'I only work on linux'
            
        
        QtCore.QThread.__init__(self)
        self.window_low = -10
        self.window_high = 10
        self.dx_old = 0
        self.dy_old = 0
        self.mouse = file('/dev/input/mouse0')
        self.xPos = 0
        self.yPos = 0
        self.recorder = recorder
        self.is_running = True
        if self.recorder:
            self.init_recorder()

    def run(self):

        while self.is_running:
                status, dx, dy = tuple(ord(c) for c in self.mouse.read(3)) 
            
                dx = self.to_signed(dx)  
                dy = self.to_signed(dy)
                dy = self.y_mov_filter(self.dy_old,dy)
                dx = self.x_mov_filter(self.dy_old,dx)
                self.dx_old=dx
                self.dy_old=dy
                self.xPos = self.xPos + dx
                self.yPos = self.yPos + dy
                if self.recorder:
                    self.rec.write(str(dx)+' '+ str(dy)+'\n')
                    
    def stop(self):
        self.is_running = False
 
    def to_signed(self,n):
            '''
            convert unsigned int to signed int
            '''
            return n - ((0x80 & n) << 1) 

    def y_mov_filter(self,old,new):
            'filter the movement in y direction'
            if new < self.window_low:
                return self.window_low
            if new > self.window_high:
                return self.window_high
            return new

    def x_mov_filter(self,old,new):
            'filter the movement in x direction'
            return new
    
    def getPos(self):
        '''
        get current x and y coordinates in the mousereader coordinate system
        '''
        return (self.xPos,self.yPos)

    def getLastDeltas(self):
        '''
        get the last observed dx, dy values of the mouse, note that
        the values are not changed (i.e. set to 0) when the mouse is not moving
        '''
        return (self.dx_old,self.dy_old)
    
    def init_recorder(self):
        self.rec = open('mousedata.txt', 'w')
        return

    
  
if __name__=='__main__':
       
        import time
        
        app = MouseReader(recorder=True)
        app.start()
        while True:
                time.sleep(.1)
                print app.getPos()
    
   
