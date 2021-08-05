from PyQt5 import QtCore, QtWidgets


class Eventandler(QtWidgets.QPushButton):
    def __init__(self, main_window, riot_event, layout_groupbox, sgroupbox):
        super().__init__()
        eventPushButtonAction = QtWidgets.QPushButton(riot_event["event_name"], sgroupbox)
        # eventPushButton.setObjectName("pushButton")
        layout_groupbox.addWidget(eventPushButtonAction)
        eventPushButtonAction.clicked.connect(self._eventActionSlot)

    def _eventActionSlot(self):
        self.uiCentralWidget = QtWidgets.QLabel("event")

        ########### event data scroll area
        main_window.eventDataScrollArea = QtWidgets.QScrollArea(self.uiCentralWidget)
        # self.eventDataScrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.eventDataScrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # (width,height_top ,width, height_bottom)
        self.eventDataScrollArea.setGeometry(QtCore.QRect(780, -2, 426, 625))
        self.eventDataScrollArea.setWidgetResizable(True)
        self.eventDataScrollArea.setObjectName("eventDataScrollArea")
        self.eventDataScrollAreaWidgetContent = QtWidgets.QWidget()
        self.eventDataScrollAreaWidgetContent.setGeometry(QtCore.QRect(0, 0, 309, 549))
        self.eventDataScrollAreaWidgetContent.setObjectName("eventDataScrollAreaWidgetContent")
        self.eventDataScrollArea.setFocusPolicy(QtCore.Qt.NoFocus)

        print("event")
