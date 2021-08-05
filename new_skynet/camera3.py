#!/usr/bin/python3
import asyncio
import http
import json
import sys
import threading
import time
import urllib.parse as urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
from urllib.parse import parse_qs

import cv2
import requests
import websocket  # client

FPS = 1
HOST, PORT = "localhost", 8080


class ECamHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        img_src = 'http://{}:{}/cam.mjpg'.format(server.server_address[0], server.server_address[1])
        self.html_page = """
            <html>
                <head></head>
                <body>
                    <img src="{}"/>
                </body>
            </html>""".format(img_src)
        self.html_404_page = """
            <html>
                <head></head>
                <body>
                    <h1>NOT FOUND</h1>
                </body>
            </html>"""
        BaseHTTPRequestHandler.__init__(self, request, client_address, server)

    def createRequest(self, url):
        parsed = urlparse.urlparse(url)
        type = (parse_qs(parsed.query)['type'])[0]
        amount = (parse_qs(parsed.query)['amount'])[0]
        transactionId = (parse_qs(parsed.query)['transactionId'])[0]

        connectionURL = (
            'https://lpn4b8754e.execute-api.us-east-1.amazonaws.com/test/test?transactionId={}&type={}&amount={}').format(
            transactionId, amount, type)

        response = requests.get(connectionURL)
        self.send_response(http.HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        text_page = """
        <html>
                <head></head>
                <body>Im on Israel cool computer but getting data from my cool aws<br/>
                {}
                </body>
        </html>""".format(response.text)

        self.wfile.write(text_page.encode())

    def do_GET(self):
        if self.path.startswith('/testGET'):
            self.createRequest(self.path)

        elif self.path.startswith('/testWS'):
            if (serverSocket):
                asyncio.get_event_loop().run_until_complete(self.createWSRequest())

        elif self.path.endswith('.mjpg'):
            self.send_response(http.HTTPStatus.OK)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    img = self.server.read_frame()
                    retval, jpg = cv2.imencode('.jpg', img)
                    if not retval:
                        raise RuntimeError('Could not encode img to JPEG')
                    jpg_bytes = jpg.tobytes()
                    self.wfile.write("--jpgboundary\r\n".encode())
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', len(jpg_bytes))
                    self.end_headers()
                    self.wfile.write(jpg_bytes)
                    time.sleep(self.server.read_delay)
                except (IOError, ConnectionError):
                    break
        elif self.path.endswith('.jpg'):
            self.send_response(http.HTTPStatus.OK)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            try:
                img = self.server.read_frame()
                retval, jpg = cv2.imencode('.jpg', img)
                if not retval:
                    raise RuntimeError('Could not encode img to JPEG')
                jpg_bytes = jpg.tobytes()
                self.wfile.write("--jpgboundary\r\n".encode())
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', len(jpg_bytes))
                self.end_headers()
                self.wfile.write(jpg_bytes)
            except (IOError, ConnectionError):
                print("ERROR {}", IOError)
        elif self.path.endswith('.html'):
            self.send_response(http.HTTPStatus.OK)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.html_page.encode())
        elif self.path.endswith('notification'):
            print("GOT notification")
        # do some UI logic
        else:
            self.send_response(http.HTTPStatus.NOT_FOUND)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(self.html_404_page.encode())


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

    def __init__(self, capture_path, server_address, RequestHandlerClass, bind_and_activate=True):
        HTTPServer.__init__(self, server_address, RequestHandlerClass, bind_and_activate)
        ThreadingMixIn.__init__(self)
        # try:
        # verifies whether is a webcam
        #	capture_path = int(capture_path)
        # except TypeError:
        #			pass
        self._capture_path = capture_path
        fps = 30
        self.read_delay = int(FPS) / fps
        self._lock = threading.Lock()
        self._camera = cv2.VideoCapture(capture_path)

    def open_video(self):
        if not self._camera.open(self._capture_path):
            raise IOError('Could not open Camera {}'.format(self._capture_path))

    def read_frame(self):
        with self._lock:
            retval, img = self._camera.read()
            if not retval:
                self.open_video()
        return img

    def serve_forever(self, poll_interval=0.5):
        self.open_video()
        try:
            super().serve_forever(poll_interval)
        except KeyboardInterrupt:
            self._camera.release()


def on_open(ws):
    print('websocket opened')
    createWSRequest(ws)


def on_error(ws, error):
    print('websocket error')
    print(error)


def on_message(ws, message):
    print('websocket message')
    print(message)


def on_close(ws, close_status_code, close_msg):
    print('websocket closed')


def connectWS():
    uri = "wss://5uhy9pq6qc.execute-api.us-east-1.amazonaws.com/production"
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(uri,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever()
    #
    #
    # https://5uhy9pq6qc.execute-api.us-east-1.amazonaws.com/production/@connections
    # global serverSocket
    # serverSocket = await websockets.connect(uri)
    # await createWSRequest()


def createWSRequest(ws):
    msgToSend = json.dumps({
        "action": "onmessage",
        "data": "bla2"
    })

    ws.send(
        msgToSend
    )


# async with websockets.connect(uri) as websocket:
#   return
# name = "Israels client"

# await websocket.send(name)
# print(f"> {name}")

# greeting = await websocket.recv()
# print(f"< {greeting}")

serverSocket = False


async def main():
    if (len(sys.argv) > 1):
        pipe = sys.argv[1]
    else:
        # 0 means USB camera,
        # can also be mjpeg camera with: 'http://wmccpinetop.axiscam.net/mjpg/video.mjpg'
        # or ip camera with 'rtsp://192.168.1.64/1'
        # or file with 'bunny.mp4'
        # pipe = 0
        pipe = 'bunny.mp4'

    # server = ThreadedHTTPServer(pipe, (HOST, PORT), ECamHandler)
    connectWS()
    # asyncio.get_event_loop().run_until_complete(connectWS(server))

    print("server started")
    # server.serve_forever()


# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#		print(bucket.name)

# Upload a new file
#	data = open('test.jpg', 'rb')
#	s3.Bucket('my-bucket').put_object(Key='test.jpg', Body=data)


if __name__ == '__main__':
    # main()
    asyncio.get_event_loop().run_until_complete(main())
