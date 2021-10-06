from threading import Thread
from copy import deepcopy
import queue
import cv2
import simplejpeg

class Camera(Thread):
    def __init__(self, cam):
        Thread.__init__(self)
        self.__cam = cam
        self.__shouldStop = False
        
    def __del__(self):
        self.__cam.release()
        print('Camera released')
    
    def get_frame(self):
        rval, frame = self.__cam.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def stopCamera(self):
        self.__shouldStop = True