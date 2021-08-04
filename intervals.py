from threading import Thread
from time import sleep

#!/usr/bin/python3
import requests
import json
import time
from colabreq import ColabRequestClass

class IntervalsClass():
    def __init__(self, intervalTime, notifications, camera, picture):
        print('loading IntervalsClass')
        self.intervalTime = intervalTime
        self.notifications = notifications
        self.camera = camera
        self.picture = picture

    def checkForNotifications(self):
        time.sleep(self.intervalTime)
        try:
            notification = ColabRequestClass.checkNotification()
        except (IOError, ConnectionError):
            print("error getting notification")
        self.checkForNotifications()

    def updateVideoInUI(self):
        time.sleep(self.intervalTime)
        try:
            print("updating UI")
            self.updateVideoInUI()
        except (IOError, ConnectionError):
            print("error getting notification")

    def sendPicture(self):
        time.sleep(self.intervalTime)
        try:
            picture = "sdfsdfsdf"
            pictureResult = ColabRequestClass.sendPicture(picture)
        except (IOError, ConnectionError):
            print("error getting picture result")

    def startIntervals(self):
        notificationsThread = Thread(target=self.checkForNotifications)
        videoThread = Thread(target=self.updateVideoInUI)
        sendPictureThread = Thread(target=self.sendPicture)
        notificationsThread.start()
        videoThread.start()
        sendPictureThread.start()
