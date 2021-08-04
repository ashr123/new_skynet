

#!/usr/bin/python3
import requests
import json
import time
import cv2
import threading
from colabreq import ColabRequestClass

class CameraClass():
    FPS = 1

    def __init__(self, fps = 30, pipe = 'bunny.mp4'):
        print('loading CameraClass')
        self._pipe = pipe
        self._fps = fps
        self._read_delay = int(CameraClass.FPS) / fps
        self._lock = threading.Lock()
        self._camera = cv2.VideoCapture(pipe)
        self._frameId = 0

    def open_video(self):
        if not self._camera.open(self._pipe):
            raise IOError('Could not open Camera {}'.format(self._pipe))

    def read_frame(self):
        with self._lock:
            retval, img = self._camera.read()
            if not retval:
                self.open_video()
        return img

    def get_picture(self):
        self._frameId = self._frameId + 1
        img = self.read_frame()
        retval, jpg = cv2.imencode('.jpg', img)
        if not retval:
            raise RuntimeError('Could not encode img to JPEG')
        if self._frameId > 10000:
            self._frameId = 1
        return jpg, self._frameId
