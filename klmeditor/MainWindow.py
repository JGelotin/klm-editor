import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)
        self.show()

        self.openButton.clicked.connect(self.openFileDialog)
        self.exitButton.clicked.connect(self.close)
        
    def openFileDialog(self):
        fn = QFileDialog.getOpenFileName()
        split_fn = os.path.splitext(fn[0])

        file_name = split_fn[0]
        file_extension = split_fn[1]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())
