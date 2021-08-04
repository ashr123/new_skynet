import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, Qt, QtMultimedia, QtMultimediaWidgets
from main_window_ui import Ui_MainWindow
from video_thread import VideoThread, VideoApp
import numpy as np
import cv2

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.currentEvents = []
        self.riot_event_counter = 0
        self.riot_events = dict()

        self._connections()
        # event = QtWidgets.QLabel("Event 1")
        event1 = {
            "event_name": "Event {}".format(self.riot_event_counter+1),
            "event_data": "Event number: {}\nDate: 4.8.2021 12:36".format(self.riot_event_counter)
        }
        event2 = {
            "event_name": "Event {}".format(self.riot_event_counter + 2),
            "event_data": "Event number: {}\nDate: 4.8.2021 20:36".format(self.riot_event_counter)
        }
        self.currentEvents.append(event1)
        self._addEventsToolBarActionSlot(event1)
        self.create_event_button(event1)
        self.create_event_button(event2)
        self.creadVideoThreadWidget()


    def creadVideoThreadWidget(self):
        self.video_output = VideoApp()
        self.videoLayoutArea = QtWidgets.QVBoxLayout(self.uiCentralWidget)
        self.videoLayoutArea.addWidget(self.video_output)

    def create_event_layout_container(self):
        self.eventsLayoutArea = QtWidgets.QVBoxLayout()
        # self.eventsScrollAreaWidgetContents.setLayout(self.eventsLayoutArea)
        # self.scrollAreaWidgetContents.setLayout(self.eventLayoutArea)
        self.eventsScrollArea.setWidget(self.eventsScrollAreaWidgetContents)

    def create_eventData_layout_container(self):
        self.eventDataLayoutArea = QtWidgets.QVBoxLayout()
        self.eventDataScrollAreaWidgetContent.setLayout(self.eventDataLayoutArea)
        # self.scrollAreaWidgetContents.setLayout(self.eventLayoutArea)
        self.eventDataScrollArea.setWidget(self.eventDataScrollAreaWidgetContent)

    def create_event_layout_group(self, riot_event):
        self.sgroupbox_events = QtWidgets.QGroupBox("Events:", self)
        self.layout_events_groupbox = QtWidgets.QVBoxLayout(self.sgroupbox_events)
        # eventPushButtonAction = QtWidgets.QPushButton(riot_event["event_name"], sgroupbox)
        # # eventPushButtonAction.setObjectName("eventPushButton")
        # layout_groupbox.addWidget(eventPushButtonAction)
        # eventPushButtonAction.clicked.connect( lambda event_clicked: self._eventActionSlot(riot_event))

    def create_eventData_layout_group(self, riot_event):
        self.sgroupbox_eventData = QtWidgets.QGroupBox("Event Data:", self)
        self.layout_eventData_groupbox = QtWidgets.QVBoxLayout(self.sgroupbox_eventData)
        event_data = QtWidgets.QLabel(riot_event["event_data"])
        self.layout_eventData_groupbox.addWidget(event_data)
        self.layout_eventData_groupbox.addStretch(1)

    def create_event_button(self, riot_event):
        self.riot_event_counter += 1
        # row = QtWidgets.QHBoxLayout()
        eventPushButtonAction = QtWidgets.QPushButton("Event {}".format(self.riot_event_counter), self.sgroupbox_events)
        eventPushButtonAction.clicked.connect(lambda event_clicked: self._eventActionSlot(riot_event))
        # eventPushButtonAction.setObjectName("eventPushButton")
        # row.addWidget(eventPushButtonAction)
        # self.layout_events_groupbox.layout().addLayout(row)
        self.layout_events_groupbox.addWidget(eventPushButtonAction)
        self.layout_events_groupbox.addStretch(1)
        self.eventsScrollAreaWidgetContents.setLayout(self.eventsLayoutArea)


    def _startActionSlot(self):
        print("start")

    def _addEventsToolBarActionSlot(self, riot_event):
        self.create_event_layout_container()
        self.create_event_layout_group(riot_event)
        self.eventsLayoutArea.addWidget(self.sgroupbox_events)

    def _showEventData(self, riot_event):
        self.create_eventData_layout_container()
        self.create_eventData_layout_group(riot_event)
        self.eventDataLayoutArea.addWidget(self.sgroupbox_eventData)

        # pass
    def _eventActionSlot(self, riot_event):
        # self.uiCentralWidget = QtWidgets.QLabel("event")
        self._showEventData(riot_event)
        print("{}".format(riot_event["event_name"]))


    def _connections(self):
        """
        Connect widgets to slots
        """
        # menuToolBar connections
        self.uiHomePageAction.triggered.connect(self._startActionSlot)
        # self.scrollArea.aboutToShow.connect(self._addEventsForEventToolBarActionSlot)



        # eventToolBar connections

    def closeEvent(self, event):
        replay = QtWidgets.QMessageBox.question(self, 'Window Close', 'Are you sure you want to close the window?',
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if replay == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


    def keyPressEvent(self, event):
        print(event.text())
        if event.key() == QtCore.Qt.Key_Space:
            print('space key was pressed')



