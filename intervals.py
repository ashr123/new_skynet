rom
threading
# !/usr/bin/python3
import time
from threading import Thread

import Thread

from colabreq import ColabRequestClass
from new_skynet.camera4 import CameraClass


# !/usr/bin/python3


class IntervalsClass():
    def __init__(self, intervalTime, notifications, camera, picture):
        print('loading IntervalsClass')
        self.intervalTime = intervalTime
        self.notifications = notifications
        self.camera = camera
        self.picture = picture
        self.cameraHandler = CameraClass(30, './new_skynet/bunny.mp4')
        #self.cameraHandler = CameraClass(30, 0)

    def checkForNotifications(self):
        time.sleep(self.intervalTime*5)
        try:
            notification = ColabRequestClass.checkNotification()
        except (IOError, ConnectionError):
            print("error getting notification")
        self.checkForNotifications()

    def updateVideoInUI(self, picture):
        try:
            print("updating UI")
        except (IOError, ConnectionError):
            print("error getting notification")

    def doPicture(self, window):
        time.sleep(self.cameraHandler._read_delay)
        try:
            picture, frameId = self.cameraHandler.get_picture()
            self.updateVideoInUI(picture)
            if self.cameraHandler._frameId % self.cameraHandler._fps == 0:
                pictureResult = ColabRequestClass.sendPicture(picture, frameId)
        except (IOError, ConnectionError):
            print("error getting picture result")
        self.doPicture()

    def startIntervals(self, mainwindow):
        notificationsThread = Thread(target=self.checkForNotifications)
        # videoThread = Thread(target=self.updateVideoInUI)
        doPictureThread = Thread(mainwindow, target=self.doPicture)
        notificationsThread.start()
        # videoThread.start()
        doPictureThread.start()
