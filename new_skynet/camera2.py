#!/usr/bin/python
import time

import StringIO
import cv2
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from PIL import Image
from SocketServer import ThreadingMixIn

capture = None
HOST, PORT = "localhost", 8080
MJPEG_SLEEP_INTERVAL = 0.05


class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('notification'):
            print("GOT notification")
            # do some UI logic
            return
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc, img = capture.read()
                    if not rc:
                        continue
                    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                    jpg = Image.fromarray(imgRGB)
                    tmpFile = StringIO.StringIO()
                    jpg.save(tmpFile, 'JPEG')
                    self.wfile.write("\r\n--jpgboundary\r\n")
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(tmpFile.len))
                    self.end_headers()
                    jpg.save(self.wfile, 'JPEG')
                    time.sleep(MJPEG_SLEEP_INTERVAL)
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.jpg'):
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=jpgboundary')
            self.end_headers()
            try:
                rc, img = capture.read()
                imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                jpg = Image.fromarray(imgRGB)
                tmpFile = StringIO.StringIO()
                jpg.save(tmpFile, 'JPEG')
                self.wfile.write("\r\n--jpgboundary\r\n")
                self.send_header('Content-type', 'image/jpeg')
                self.send_header('Content-length', str(tmpFile.len))
                self.end_headers()
                jpg.save(self.wfile, 'JPEG')
            except KeyboardInterrupt:
                print("BREAK")
            return
        if self.path.endswith('.html'):
            imageStr = '<img src="http://{}:{}/cam.mjpg"/>'.format(HOST, PORT)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('<html><head></head><body>')
            self.wfile.write(imageStr)
            self.wfile.write('</body></html>')
            return


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""


def main():
    global capture
    # 0 means USB camera,
    # can also be mjpeg camera with: 'http://wmccpinetop.axiscam.net/mjpg/video.mjpg'
    # or ip camera with 'rtsp://192.168.1.64/1'
    # or file with 'test.mp4'
    pipe = 0

    capture = cv2.VideoCapture(pipe)
    global img
    try:
        server = ThreadedHTTPServer((HOST, PORT), CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()


if __name__ == '__main__':
    main()
