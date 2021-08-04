import datetime
import time
import argparse
import signal
from main_window import MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
import sys
from main_window_ui import Ui_MainWindow
from main_window import MainWindow
from colabreq import ColabRequestClass
from intervals import IntervalsClass

def main():
    # parser = argparse.ArgumentParser()
    # parser.add_argument("project", help="load a GNS3 project (.gns3)", metavar="path", nargs="?")
    # parser.add_argument("--version", help="show the version", action="version", version=__version__)
    # parser.add_argument("--debug", help="print out debug messages", action="store_true", default=False)
    # parser.add_argument("-q", "--quiet", action="store_true", help="do not show logs on stdout")
    # parser.add_argument("--config", help="Configuration file")
    # parser.add_argument("--profile", help="Settings profile (blank will use default settings files)")
    # options = parser.parse_args
    start()


def start():
    # global mainwindow
    # mainwindow = MainWindow()
    # mainwindow.show()
    ColabRequestClass.getColabURL()
    p1 = IntervalsClass(1, True, True, True)
    p1.startIntervals()

    #ColabRequestClass.sendPicture("sdfsdfsdfsdf")
    #ColabRequestClass.checkNotification()
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Fusion')
    mainwindow = MainWindow()
    mainwindow.show()

    sys.exit(app.exec_())








if __name__ == "__main__":
    main()

