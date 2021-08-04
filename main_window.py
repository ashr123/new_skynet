from PyQt5 import QtCore, QtGui, QtWidgets

from main_window_ui import Ui_MainWindow


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        self.currentEvents = []
        self.riot_event_counter = 0
        self.riot_events = dict()

        # event = QtWidgets.QLabel("Event 1")

        self._connections()


    def creadVideoThreadWidget(self):
        # self.video_output = VideoApp()
        # update widget
        pixmap = QtGui.QPixmap(r'C:\Users\Yael\Desktop\elbit\skynet_hackaton\new-skynet\img\riot_ai_fire.png')
        self.video_label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

    def create_event_layout_container(self):
        self.eventsLayoutArea = QtWidgets.QVBoxLayout(self.eventsScrollAreaWidgetContents)
        self.eventsLayoutArea.addItem(
            QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        self.eventsScrollArea.setWidget(self.eventsScrollAreaWidgetContents)

    def create_button(self, riot_event):
        count = self.eventsLayoutArea.count() - 1  # -1 is to make place the buttons from the top
        groupbox_events = QtWidgets.QGroupBox("".format(count), self.eventsScrollArea)
        self.eventsLayoutArea.insertWidget(count, groupbox_events)
        gridLayout = QtWidgets.QGridLayout(groupbox_events)
        eventPushButtonAction = QtWidgets.QPushButton("Event {}".format(count))
        gridLayout.addWidget(eventPushButtonAction, 0, 0, 1, 1)
        data_text = self._showEventData(riot_event)
        eventPushButtonAction.clicked.connect(lambda: self.event_data.setText(data_text))


    def _startActionSlot(self):
        self.event_data.hide()
        # print("start")

    def _showEventData(self, riot_event):
        self.event_data.show()
        return riot_event["event_data"]

    def _connections(self):
        """
        Connect widgets to slots
        """
        # menuToolBar connections
        event1 = {
            "event_name": "Event {}".format(self.riot_event_counter + 1),
            "event_data": "Event number: {}\nDate: 4.8.2021 12:36".format(self.riot_event_counter)
        }
        event2 = {
            "event_name": "Event {}".format(self.riot_event_counter + 2),
            "event_data": "Event number: {}\nDate: 4.8.2021 20:36".format(self.riot_event_counter)
        }
        self.uiHomePageAction.triggered.connect(lambda: self.create_button(event1))
        self.uiHome2PageAction.triggered.connect(lambda: self.create_button(event2))
        self.uiHome3PageAction.triggered.connect(lambda: self._startActionSlot)
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
