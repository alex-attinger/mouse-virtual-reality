import pygame
import pygame.camera
from pygame.locals import *
import cv as cv
import cv2
import time
import sys
from pygame import surfarray
import pygame.image

#if __name__ == '__main__':
#    size = (640, 480)
#    pygame.camera.init()
#    cam = pygame.camera.Camera('/dev/video0', size)
#    cv.NamedWindow('w', cv.CV_WINDOW_AUTOSIZE)
#    cam.start()
#    print cam.get_size()
#    print len(cam.get_raw())
#    cv_im = cv.CreateImageHeader(size, cv.IPL_DEPTH_8S, 3)
#   
#    cv.SetData(cv_im,cam.get_raw())
#    cv.SaveImage('test.png', cv_im)
#
#
#    cam.stop()


dtype2depth = {
        'uint8':   cv.IPL_DEPTH_8U,
        'int8':    cv.IPL_DEPTH_8S,
        'uint16':  cv.IPL_DEPTH_16U,
        'int16':   cv.IPL_DEPTH_16S,
        'int32':   cv.IPL_DEPTH_32S,
        'float32': cv.IPL_DEPTH_32F,
        'float64': cv.IPL_DEPTH_64F
    }

if __name__ == '__main__':
    pygame.camera.init()
    
    size = (640, 480)
    cam = pygame.camera.Camera('/dev/video0', size)
    cam.start()
    
    snapshot = pygame.surface.Surface(size, 0, depth = 32)
    
    snapshot=cam.get_image(snapshot)
    for i in range(1000):
        pygame.image.save(snapshot, 'z%04d.bmp'%(i))
        
    
#    pixarr = pygame.surfarray.pixels3d(snapshot)
#
#    a = pixarr.transpose(1,0,2)
#    cv_im = cv.CreateImageHeader((a.shape[1],a.shape[0]),
#          dtype2depth[str(a.dtype)],
#          3)
#          
#    
#    cv.SetData(cv_im, a.tostring(),
#             a.dtype.itemsize*3*a.shape[1])
    
    #cv_im = cv.fromarray(p)
    
    
    
    #cv.SaveImage('test.png', cv_im)
    cam.stop()
    
    

