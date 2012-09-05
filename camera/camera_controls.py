import gst
from PyQt4.QtGui import QMainWindow, QWidget, QApplication, QPushButton
import sys
import os
import subprocess

class Controls(QMainWindow):
    '''
    show controls to control webcam 
    '''
    
    def __init__(self):
        QMainWindow.__init__(self)
        container = QWidget()
        self.setCentralWidget(container)
       
        self.setGeometry(300,300,600,600)
        self.button_text={'on':'Autofocus on', 'off': 'Autofucus off'}
        self.button = QPushButton(self.button_text['on'], self)
        self.button.setGeometry(20, 20, 100, 20)
        self.button.clicked.connect(self.toggle_autofocus)
        self.autofocus = True
        
        
        self.show()
        
    def toggle_autofocus(self):
        if self.autofocus:
            os.system
        
