import pygame
import pygame.camera
from pygame.time import Clock
from pygame.locals import *
import pygame.time
import cv
import cv2

class Capture(object):
    def __init__(self):
        #self.size = (1280,720)
        self.size = (640, 480)
        self.clock = Clock()
        self.fps = 25
        # create a display surface. standard pygame stuff
        self.display = pygame.display.set_mode(self.size, 0)
        self.frameno = 1
        # this is the same as what we saw before
        self.clist = pygame.camera.list_cameras()
        if not self.clist:
            raise ValueError("Sorry, no cameras detected.")
        self.cam = pygame.camera.Camera(self.clist[0], self.size)
        self.cam.start()
       
        # create a surface to capture to.  for performance purposes
        # bit depth is the same as that of the display surface.
        self.snapshot = pygame.surface.Surface(self.size, 0, self.display)
        pygame.time.set_timer(USEREVENT+ 1, 40)
       
#self.rec=cv.CreateVideoWriter('/home/mouse/Desktop/VR/camera/test.avi',cv.CV_FOURCC('M','P','1','V'),  self.fps, self.size, 1)
#
#self.cv_im = cv.CreateImageHeader(self.size,
#  cv.IPL_DEPTH_8U,
#  3)

    def get_and_flip(self):
        
        # if you don't want to tie the framerate to the camera, you can check 
        # if the camera has an image ready.  note that while this works
        # on most cameras, some will never return true.
        if self.cam.query_image():
            self.snapshot = self.cam.get_image(self.snapshot)
        
#        pixarr = pygame.surfarray.array3d(self.snapshot)
#        arr = pixarr.transpose(1, 0, 2)
        
        
       
          
    
#        cv.SetData(self.cv_im, arr.tostring(),arr.dtype.itemsize*3*arr.shape[1])
#       
#        cv.WriteFrame(self.rec, self.cv_im)
        #
        # blit it to the display surface.  simple!
       
        self.display.blit(self.snapshot, (0,0))
        #self.clock.tick(self.fps)
        pygame.display.flip()
        
    def record(self):
        pygame.image.save(self.snapshot, 'vid/%05d.bmp'%self.frameno)
        self.frameno += 1

    def main(self):
        going = True
        while going:
            events = pygame.event.get()
            for e in events:
                if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
                    # close the camera safely
                    self.cam.stop()
                    going = False
                elif e.type == (USEREVENT +1):
                    self.record()

            self.get_and_flip()


if __name__ == '__main__':
    pygame.init()
    pygame.camera.init()
    myapp = Capture()
    myapp.main()
