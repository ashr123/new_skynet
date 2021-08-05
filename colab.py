import json
import time
import urllib.error
import urllib.request
from threading import Thread
from time import sleep

import requests  # Import the requests library
# flask_ngrok_example.py
from flask import Flask, request, jsonify
from flask_ngrok import run_with_ngrok


def threaded_function():
    sleep(10)
    print("running")


app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
run_with_ngrok(app)  # Start ngrok when app is run

mypicture = "bababbaba"


def checkMyAddress():
    ngrokAPIURL = 'http://127.0.0.1:4040/api/tunnels'
    time.sleep(5)
    try:
        conn = urllib.request.urlopen(ngrokAPIURL)
    except urllib.error.HTTPError as e:
        # Email admin / log
        print(f'HTTPError: for {url}')
        time.sleep(5)
        checkMyAddress()
    except urllib.error.URLError as e:
        # Email admin / log
        print(f'URLError: for {url}')
        time.sleep(5)
        checkMyAddress()
    else:
        # Website is up
        ngrokURI = !curl - -silent - -show - error
        http: // 127.0
        .0
        .1: 4040 / api / tunnels | sed - nE
        's/.*public_url":"https:..([^"]*).*/\1/p'
        ngrokURI = """http://{}""".format(ngrokURI[0])
        print(ngrokURI)

        data = {'ngrokAddr': ngrokURI}
        data = json.dumps(data)

        r = requests.post('https://lpn4b8754e.execute-api.us-east-1.amazonaws.com/test/test', data)
        if r.status_code == 200 and r.ok == True:
            result = json.loads(r.text)
            if result['body'] != ngrokURI:
                print('uploading ngrok address failed')
            else:
                print('uploading ngrok address worked')
        else:
            print('uploading ngrok address failed')


@app.route("/")
def hi():
    return "Welcome"


@app.route("/checkNotifications")
def checkNotifications():
    dictToReturn = {'answer': 42}
    return jsonify(dictToReturn)


@app.route("/predictionResult")
def getPredictionFromMemory():
    return mypicture


@app.route('/sendPicture', methods=['POST'])
def sendPicture():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer
    # forgot to set the MIME type to 'application/json'
    print('data from client:')
    print(input_json)
    sleep(5)
    dictToReturn = {'answer': 42}
    return jsonify(dictToReturn)


def welcome():
    print('Welcome!')


if __name__ == '__main__':
    thread = Thread(target=checkMyAddress)
    thread.start()
    app.run()

    # If address is in use, may need to terminate other sessions:
    # Runtime > Manage Sessions > Terminate Other Sessions
