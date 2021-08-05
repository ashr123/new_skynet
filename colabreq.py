#!/usr/bin/python3
import json
import os

import requests


class ColabRequestClass():
    colabUrl = None

    def __init__(self):
        colabUrl = ColabRequestClass.getColabURL()
        print('loading ColabRequestClass')

    @staticmethod
    def getColabURL():
        try:
            r = requests.get('https://lpn4b8754e.execute-api.us-east-1.amazonaws.com/test/test')
            if r.status_code == 200:
                if r.text == "":
                    print("error getting address, using env var")
                    return os.environ.get('ngrokAddr')
                else:
                    return r.text
            else:
                return None
        except (IOError, ConnectionError):
            print("error getting address, using env var")
            return os.environ.get('ngrokAddr')

    @staticmethod
    def sendPicture(picture):
        # testing upload address post
        # data = {'ngrokAddr': "blabla"}
        # data = json.dumps(data)
        # r = requests.post('https://lpn4b8754e.execute-api.us-east-1.amazonaws.com/test/test', data)
        # test = json.loads(r.text)
        # colabUrl = ColabRequestClass.getColabURL()
        if ColabRequestClass.colabUrl == None:
            return None
        fullLink = """{}/sendPicture""".format(ColabRequestClass.colabUrl)
        data = {'picture': picture}
        data = json.dumps(data)
        try:
            # 7 seconde timeout
            result = requests.post(fullLink, data, 7)
            if result.ok == True and result.status_code == 200:
                resultJson = json.loads(result.text)
                answer = resultJson['answer']
                # todo: do something with "answer"
                print(answer)
                return answer
            else:
                print("error sending picture to colab server")
                return None
        except (IOError, ConnectionError):
            print("error sending picture to colab server")
            return None

    @staticmethod
    def checkNotification():
        # colabUrl = ColabRequestClass.getColabURL()
        if ColabRequestClass.colabUrl == None:
            return None
        fullLink = """{}/checkNotifications""".format(ColabRequestClass.colabUrl)
        try:
            # 7 seconde timeout
            result = requests.get(fullLink)
            if result.ok == True and result.status_code == 200:
                resultJson = json.loads(result.text)
                answer = resultJson['answer']
                # todo: do something with "answer"
                print(answer)
                return answer
            else:
                print("error sending picture to colab server")
                return None
        except (IOError, ConnectionError):
            print("error sending picture to colab server")
            return None
