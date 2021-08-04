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
       #### creating the events layout area:
        self.eventsLayoutArea = QtWidgets.QVBoxLayout(self.eventsScrollAreaWidgetContents)
        self.eventsLayoutArea.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.eventsScrollArea.setWidget(self.eventsScrollAreaWidgetContents)


        self._connections()

        # self.create_event_button(event1)
        # self.create_event_button(event2)
        # self.creadVideoThreadWidget()



    def creadVideoThreadWidget(self):
        self.video_output = VideoApp()
        # self.videoLayoutArea = QtWidgets.QVBoxLayout(self.uiCentralWidget)
        # self.videoLayoutArea.addWidget(self.video_output)

    def create_event_layout_container(self):
        self.eventsLayoutArea = QtWidgets.QVBoxLayout(self.eventsScrollAreaWidgetContents)
        self.eventsLayoutArea.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.eventsScrollArea.setWidget(self.eventsScrollAreaWidgetContents)

    def create_eventData_layout_container(self):

        self.eventDataLayoutArea = QtWidgets.QVBoxLayout(self.eventDataScrollAreaWidgetContent)
        self.eventDataLayoutArea.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.eventDataScrollArea.setWidget(self.eventDataScrollAreaWidgetContent)

    def create_button(self, riot_event):
        count = self.eventsLayoutArea.count() - 1 # -1 is to make place the buttons from the top
        groupbox_events = QtWidgets.QGroupBox("".format(count), self.eventsScrollArea)
        self.eventsLayoutArea.insertWidget(count, groupbox_events)
        gridLayout = QtWidgets.QGridLayout(groupbox_events)
        eventPushButtonAction = QtWidgets.QPushButton("Event {}".format(count+1), groupbox_events)
        gridLayout.addWidget(eventPushButtonAction, 0, 0, 1, 1)
        eventPushButtonAction.clicked.connect(lambda event_clicked: self._eventActionSlot(riot_event))


    def show_eventData_layout_group(self, riot_event):
        count = self.eventDataLayoutArea.count() - 1
        groupbox_eventData = QtWidgets.QGroupBox("Event Data:", self.eventDataScrollArea)
        self.eventDataLayoutArea.insertWidget(count, groupbox_eventData)
        gridLayout = QtWidgets.QGridLayout(groupbox_eventData)
        # self.layout_eventData_groupbox = QtWidgets.QVBoxLayout(groupbox_eventData)
        event_data = QtWidgets.QLabel(riot_event["event_data"])
        gridLayout.addWidget(event_data, 0, 0, 1, 1)
        # self.layout_eventData_groupbox.addWidget(event_data)
        # self.layout_eventData_groupbox.addStretch(1)


    def _startActionSlot(self):

        print("start")

    def _addEventsToolBarActionSlot(self, riot_event):
        self.create_event_layout_container()
        # self.create_event_layout_group(riot_event)
        # self.eventsLayoutArea.addWidget(self.sgroupbox_events)

    def _showEventData(self, riot_event):
        self.create_eventData_layout_container()
        self.show_eventData_layout_group(riot_event)
        # self.eventDataLayoutArea.addWidget(self.sgroupbox_eventData)

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
        event1 = {
            "event_name": "Event {}".format(self.riot_event_counter + 1),
            "event_data": "Event number: {}\nDate: 4.8.2021 12:36".format(self.riot_event_counter)
        }
        self.uiHomePageAction.triggered.connect(lambda event_add: self.create_button(event1))
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



