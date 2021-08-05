import sys

from PyQt5 import QtWidgets

from intervals import IntervalsClass
from main_window import MainWindow

if __name__ == "__main__":
	# parser = argparse.ArgumentParser()
	# parser.add_argument("project", help="load a GNS3 project (.gns3)", metavar="path", nargs="?")
	# parser.add_argument("--version", help="show the version", action="version", version=__version__)
	# parser.add_argument("--debug", help="print out debug messages", action="store_true", default=False)
	# parser.add_argument("-q", "--quiet", action="store_true", help="do not show logs on stdout")
	# parser.add_argument("--config", help="Configuration file")
	# parser.add_argument("--profile", help="Settings profile (blank will use default settings files)")
	# options = parser.parse_args
	# global mainwindow
	# mainwindow = MainWindow()
	# mainwindow.show()

	p1 = IntervalsClass(3, True, True, True)
	p1.startIntervals()
	# ColabRequestClass.sendPicture("sdfsdfsdfsdf")
	# ColabRequestClass.checkNotification()
	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	MainWindow().show()

	sys.exit(app.exec_())