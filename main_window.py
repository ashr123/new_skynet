import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from main_window_ui import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.pushButtonsEvents = dict()
        self.event_counter = 0
        self.events = dict()

        self._connections()
        # event = QtWidgets.QLabel("Event 1")
        event = {
            "event_name": "Event {}".format(self.event_counter+1),
            "event_signal_action": ""
        }
        self._addEventsForEventToolBarActionSlot(event["event_name"])
        # self.layoutArea.addStretch(1)

        # self._addEventsForEventToolBarActionSlot(event)

    def create_layout_container(self, event):
        self.layoutArea = QtWidgets.QVBoxLayout()
        self.scrollAreaWidgetContents.setLayout(self.layoutArea)
        self.scrollAreaWidgetContents.setLayout(self.layoutArea)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

    def create_layout_group(self, event):
        sgroupbox = QtWidgets.QGroupBox("Events:", self)
        layout_groupbox = QtWidgets.QVBoxLayout(sgroupbox)
        self.event_counter += 1
        eventPushButtonAction = QtWidgets.QPushButton(event, sgroupbox)
        # eventPushButton.setObjectName("pushButton")
        layout_groupbox.addWidget(eventPushButtonAction)
        eventPushButtonAction.clicked.connect(self._eventActionSlot)
        # eventPushButtonAction.hide()
        # eventPushButton.setGeometry(QtCore.QRect(60, 80, 201, 31))
        layout_groupbox.addStretch(1)

        # eventPushButton.setObjectName("pushButton")
        # layout_groupbox = QtWidgets.QVBoxLayout(sgroupbox)

        return sgroupbox


    def _startActionSlot(self):
        print("start")

    def _addEventsForEventToolBarActionSlot(self, event):
        self.create_layout_container(event)
        self.layoutArea.addWidget(self.create_layout_group(event))
        # pass
    def _eventActionSlot(self):
        self.uiCentralWidget = QtWidgets.QLabel("event")
        print("event")
        pass

    def _connections(self):
        """
        Connect widgets to slots
        """
        # menuToolBar connections
        self.uiHomePageAction.triggered.connect(self._startActionSlot)
        # self.scrollArea.aboutToShow.connect(self._addEventsForEventToolBarActionSlot)


        # eventToolBar connections



