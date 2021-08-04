import json
import os
import time
import requests  # Import the requests library
import urllib.request
import urllib.error
import asyncio
import threading
# flask_ngrok_example.py
from flask import Flask, render_template, request, url_for, jsonify
from flask_ngrok import run_with_ngrok
from threading import Thread
from time import sleep


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


@app.route("/")
def hi():
    return "Welcome"


@app.route("/sendPicture1")
def hello():
    global mypicture
    mypicture = "lalalallalala"
    # time.sleep(2)
    return "Picture recived"


@app.route("/predictionResult")
def getPredictionFromMemory():
    return mypicture


@app.route('/sendPicture2', methods=['POST'])
def my_test_endpoint():
    input_json = request.get_json(force=True)
    # force=True, above, is necessary if another developer 
    # forgot to set the MIME type to 'application/json'
    print('data from client:')
    print(input_json)
    dictToReturn = {'answer': 42}
    return jsonify(dictToReturn)


def test():
    print('hi')


if __name__ == '__main__':
    thread = Thread(target=checkMyAddress)
    thread.start()
    app.run()

    # If address is in use, may need to terminate other sessions:
    # Runtime > Manage Sessions > Terminate Other Session