############################################################
# Copyright (c) 2022 KLM Editor                            #
############################################################
# Authors: Kelly Vu, Guanlin Wang, Joel Allan Gelotin      #
############################################################
# Description: Entry point main function for KLM Editor    #
#                                                          #
############################################################

import sys
from MainWindow import Ui_MainWindow
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())