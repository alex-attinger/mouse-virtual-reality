import gobject, pygst
pygst.require('0.10')
import gst
from PyQt4.QtGui import QMainWindow, QWidget, QApplication 
import sys


class Video(QMainWindow):
    '''
    show and record video from webcam
    '''
    
    def __init__(self):
        QMainWindow.__init__(self)
        container = QWidget()
        self.setCentralWidget(container)
        self.windowId = container.winId()
        self.setGeometry(300,300,640,480)
        self.show()

    def setUpGst(self):
        self.player = gst.Pipeline("player")
        source = gst.element_factory_make("v4l2src", "vsource")
        source.set_property("device", "/dev/video1")
        
        sink = gst.element_factory_make("xvimagesink", "sink")
        sink.set_property("sync", 'False')
        #the timer
        timeover = gst.element_factory_make("timeoverlay", "timer")
        timeover.set_property('valign', 'bottom')
        
        #the scaler
        fvidscale_cap = gst.element_factory_make("capsfilter", "fvidscale_cap")
        fvidscale = gst.element_factory_make("videoscale", "fvidscale")
        caps = gst.caps_from_string('video/x-raw-yuv,width=640,height=480,framerate=30/1')
        fvidscale_cap.set_property('caps', caps)
        
        #the splitter
        splitter = gst.element_factory_make("tee", 'splitter')
        splitter.set_property("name", 'splitter')
        
        #a queue
        disp_queue = gst.element_factory_make('queue', 'disp_queue')
        vid_queue = gst.element_factory_make('queue', 'vid_queue')
        
        #the demuxer
        avimux = gst.element_factory_make('avimux', 'avimux')
        
        #the filesink
        filesink = gst.element_factory_make('filesink', 'filesink')
        filesink.set_property('location', 'test.avi')
        
        

        self.player.add(source, fvidscale, fvidscale_cap,timeover, splitter, disp_queue, vid_queue, avimux,  sink, filesink)
        #link to screen
        gst.element_link_many(source,fvidscale, fvidscale_cap, timeover, splitter, disp_queue, sink)
        #link to file
        gst.element_link_many(splitter,vid_queue, avimux,filesink )
        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message", self.on_message)
        bus.connect("sync-message::element", self.on_sync_message)

    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
            print "end of message"
        elif t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            win_id = self.windowId
            assert win_id
            imagesink = message.src
            imagesink.set_xwindow_id(win_id)

    def startPrev(self):
        self.player.set_state(gst.STATE_PLAYING)
        print "should be playing"

if __name__ == "__main__":
    gobject.threads_init()
    app = QApplication(sys.argv)
    video = Video()
    video.setUpGst()
    video.startPrev()
    sys.exit(app.exec_())
