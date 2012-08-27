from PyQt4 import QtCore


class MouseReader(QtCore.QThread):
    

    def __init__(self):
	QtCore.QThread.__init__(self)
	self.window_low = -10
	self.window_high = 10
	self.dx_old = 0
	self.dy_old = 0
	self.mouse = file('/dev/input/mouse0')
	self.xPos = 0
	self.yPos = 0

    def run(self):

	while True:
		status, dx, dy = tuple(ord(c) for c in self.mouse.read(3)) 

		dx = self.to_signed(dx)  
    		dy = self.to_signed(dy)
    		dy = self.y_mov_filter(self.dy_old,dy)
		dx = self.x_mov_filter(self.dy_old,dx)
   		self.dx_old=dx
    		self.dy_old=dy
		self.xPos = self.xPos + dx
		self.yPos = self.yPos + dy
 
	
    def to_signed(self,n):  
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
	return (self.xPos,self.yPos)

    def getLastDeltas(self):
	return (self.dx_old,self.dy_old)
	
    
  
if __name__=='__main__':
   
    import time
    
    app = MouseReader()
    app.start()
    while True:
	time.sleep(.1)
	print app.getPos()


     
