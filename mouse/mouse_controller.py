#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
ZetCode PyQt4 tutorial 

This example draws three rectangles in three
different colors. 

author: Jan Bodnar
website: zetcode.com 
last edited: September 2011
"""

import sys,time, socket
from PyQt4 import QtGui, QtCore
from mousereader import MouseReader

class MouseController(QtGui.QWidget):
    '''
    A qWidget to visualize mouse input.
    If udp is enabled, udp packages are sent to the specified address and port in interval ms
    Message format: init_time (time of instantiation) time passed since init_time (xPos,yPos)
    
    '''
    
    def __init__(self, udp=False, ip='127.0.0.1', port=12012, interval = 100):
        self.init_time = time.time()
        super(MouseController, self).__init__()
        self.udp = udp
        self.ip = ip
        self.port = port
        self.interval = interval
        self.red = QtGui.QColor(255, 0, 0)
        self.blue = QtGui.QColor(0,0,255)
        self.black = QtGui.QColor(0,0,0)
        self.white = QtGui.QColor(255,255,255,0)
        
        self.initUI()
        self.dy = 0
        self.dx = 0
        self.yPos = 0
        self.xPos = 0
        #the mouse reader
        self.mr= MouseReader(dev='/dev/input/mouse0')
        self.mr.start()
        
        #the timer
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.updateStatusBar)
        
        timer.start(500)
        if self.udp:
            self.sock = socket.socket( socket.AF_INET, # Internet
                socket.SOCK_DGRAM ) # UDP
            timer1 = QtCore.QTimer(self)
            timer1.timeout.connect(self.sendData)
            timer1.start(self.interval)

        
    def initUI(self):      

        self.setGeometry(300, 300, 512, 512)
        self.setWindowTitle('Mouse Controller')
        self.show()

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawStatusBar(qp,self.dy)
        self.drawStatusBar(qp,self.dx,y=300)
        self.displayValues(qp,'y Position',self.yPos)
        self.displayValues(qp,'x Position',self.xPos,y=80)
        qp.end()

    

    def drawStatusBar(self,qp,value,x=20,y=400,w=470,h=50,maxvalue=10,title=None):
        unit=int(w/(maxvalue+maxvalue))
        x_mid = (x+w)*.5
        
        
        #the value box
        if value == 0:
            pass
        
        elif value >0:
            qp.setPen(self.blue)
            qp.setBrush(self.blue)
            qp.drawRect(x_mid+1, y,value*unit, h)
        
        elif value < 0:
            qp.setPen(self.red)
            qp.setBrush(self.red)
            qp.drawRect(x_mid,y,value*unit-1,h)
        
        #the bounding box
        qp.setPen(self.black)
        qp.setBrush(self.white)
        qp.drawRect(x,y,w,h)
        #the midline
        x_mid = (x+w)*.5
        qp.setPen(self.black)
        qp.drawLine(x_mid,y,x_mid,y+h)
        return

    def displayValues(self,qp,name,value,x=20,y=40):
        text = str(name) + ':\t' + str(value) 
        qp.drawText(x,y,text)
        return

    def updateStatusBar(self):
        self.dy,self.dx = self.mr.getLastDeltas()
        self.xPos,self.yPos = self.mr.getPos()
        self.update()
        return

    def sendData(self):
        delta_time = time.time() - self.init_time
        msg=str(self.init_time)+'\t' + '%3.2f\t'%(delta_time)+str(self.mr.getPos())
        self.sendMsg(msg)

    def sendMsg(self, msg):
        self.sock.sendto(msg, (self.ip, self.port))
        return


class Receiver():
    def __init__(self, ip='127.0.0.1', port=12012):
        sock = socket.socket( socket.AF_INET, # Internet
                socket.SOCK_DGRAM ) # UDP
        sock.bind( (ip,port) )
        while True:
            data, add = sock.recvfrom(1024)
            print data
            
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = MouseController(udp=True)
    sys.exit(app.exec_())


