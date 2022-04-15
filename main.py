# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 30, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(160, 30, 131, 41))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(330, 30, 131, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(480, 30, 131, 41))
        self.pushButton_4.setObjectName("pushButton_4")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(10, 150, 781, 391))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalScrollBar = QtWidgets.QScrollBar(self.centralwidget)
        self.verticalScrollBar.setGeometry(QtCore.QRect(770, 151, 20, 389))
        self.verticalScrollBar.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar.setObjectName("verticalScrollBar")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 100, 651, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(670, 100, 121, 41))
        self.pushButton_5.setObjectName("pushButton_5")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(300, 30, 20, 41))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(620, 30, 20, 41))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_6.setGeometry(QtCore.QRect(650, 30, 141, 41))
        self.pushButton_6.setObjectName("pushButton_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuTest = QtWidgets.QMenu(self.menubar)
        self.menuTest.setObjectName("menuTest")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtWidgets.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionImport_db = QtWidgets.QAction(MainWindow)
        self.actionImport_db.setObjectName("actionImport_db")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit_2 = QtWidgets.QAction(MainWindow)
        self.actionQuit_2.setObjectName("actionQuit_2")
        self.menuTest.addAction(self.actionImport)
        self.menuTest.addAction(self.actionImport_db)
        self.menuTest.addSeparator()
        self.menuTest.addAction(self.actionQuit)
        self.menuTest.addAction(self.actionQuit_2)
        self.menubar.addAction(self.menuTest.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Create New"))
        self.pushButton_2.setText(_translate("MainWindow", "Open"))
        self.pushButton_3.setText(_translate("MainWindow", "Write "))
        self.pushButton_4.setText(_translate("MainWindow", "Save"))
        self.pushButton_5.setText(_translate("MainWindow", "Filter"))
        self.pushButton_6.setText(_translate("MainWindow", "Exit"))
        self.menuTest.setTitle(_translate("MainWindow", "File"))
        self.actionImport.setText(_translate("MainWindow", "Import .csv"))
        self.actionImport_db.setText(_translate("MainWindow", "Import .db"))
        self.actionQuit.setText(_translate("MainWindow", "Save"))
        self.actionQuit_2.setText(_translate("MainWindow", "Quit"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
