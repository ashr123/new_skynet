#!/usr/bin/python3
import requests
import json
import os
import base64

class ColabRequestClass():
    colabUrl=None
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
                    ColabRequestClass.colabUrl = r.text
                    return r.text
            else:
                return None
        except (IOError, ConnectionError):
            print("error getting address, using env var")
            return os.environ.get('ngrokAddr')

    @staticmethod
    def sendPicture(jpg, frameId):
        #testing upload address post
        #data = {'ngrokAddr': "blabla"}
        #data = json.dumps(data)
        #r = requests.post('https://lpn4b8754e.execute-api.us-east-1.amazonaws.com/test/test', data)
        #test = json.loads(r.text)
        #colabUrl = ColabRequestClass.getColabURL()
        if ColabRequestClass.colabUrl == None:
            return None
        fullLink = """{}/sendPicture""".format(ColabRequestClass.colabUrl)

        jpg_bytes = jpg.tobytes()
        #headers = {"Content-type": 'multipart/x-mixed-replace; boundary=--jpgboundary'}
        #self.wfile.write("--jpgboundary\r\n".encode())

        im_b64 = base64.b64encode(jpg_bytes).decode("utf8")
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        data = json.dumps({"image": im_b64, "frameId": frameId})

        try:
            #7 seconde timeout
            result = requests.post(url = fullLink, headers = headers, data = data, timeout = 7)
            if result.ok == True and result.status_code == 200:
                resultJson = json.loads(result.text)
                answer = resultJson['answer']
                #todo: do something with "answer"
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
        #colabUrl = ColabRequestClass.getColabURL()
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
                print("error getting notifications from colab server")
                return None
        except (IOError, ConnectionError):
            print("error getting notifications from colab server")
            return None