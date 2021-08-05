#!/usr/bin/python3
import cv2
import os, sys

class FilesClass():
    def __init__(self):
        print('loading FilesClass')

    @staticmethod
    def save_picture(picture, frameId):
        cameraPicsDirectory = os.path.abspath('./cameraImages/')
        filename = """{}\\image_{}.jpg""".format(cameraPicsDirectory,frameId)
        #filename = """image_{}.jpg""".format(frameId)
        cv2.imwrite(filename, picture)

