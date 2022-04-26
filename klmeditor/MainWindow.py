############################################################
# Copyright (c) 2022 KLM Editor                            #
############################################################
# Authors: Kelly Vu, Guanlin Wang, Joel Allan Gelotin      #
############################################################
# Description: This file contains the a PyQt setup user    #
# interface for KLM Editor. The functionality regarding    #
# the importing, modification, and exporting of .csv and   #
# .db files are also located here.                         #
#                                                          #
############################################################

import os
import csv
import sqlite3
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        ################################################
        #    MAIN WINDOW AND NON-FUNCTIONAL WIDGETS    #
        ################################################
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setMinimumSize(QtCore.QSize(800, 600))
        MainWindow.setMaximumSize(QtCore.QSize(800, 600))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(30, 10, 191, 71))
        font = QtGui.QFont()
        font.setFamily("Maiandra GD")
        font.setPointSize(26)
        self.nameLabel.setFont(font)
        self.nameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.nameLabel.setObjectName("nameLabel")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(420, 30, 20, 41))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(620, 30, 20, 41))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")

        ###################################
        #             BUTTONS             #
        ###################################

        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        self.openButton.setGeometry(QtCore.QRect(250, 30, 161, 41))
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(self.open_file_dialog)

        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setGeometry(QtCore.QRect(450, 30, 161, 41))
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.save_file_dialog)

        self.inputLine = QtWidgets.QLineEdit(self.centralwidget)
        self.inputLine.setGeometry(QtCore.QRect(10, 100, 581, 41))
        self.inputLine.setObjectName("inputLine")

        self.filterButton = QtWidgets.QPushButton(self.centralwidget)
        self.filterButton.setGeometry(QtCore.QRect(600, 100, 91, 41))
        self.filterButton.setObjectName("filterButton")
        self.filterButton.clicked.connect(self.filter_table)

        self.exitButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitButton.setGeometry(QtCore.QRect(650, 30, 131, 41))
        self.exitButton.setObjectName("exitButton")
        self.exitButton.clicked.connect(MainWindow.close)

        self.queryButton = QtWidgets.QPushButton(self.centralwidget)
        self.queryButton.setEnabled(True)
        self.queryButton.setGeometry(QtCore.QRect(600, 100, 91, 41))
        self.queryButton.setObjectName("queryButton")
        self.queryButton.setVisible(False)
        self.queryButton.clicked.connect(self.execute_query_from_input_line)

        self.databaseTableComboBox = QtWidgets.QComboBox(self.centralwidget)
        self.databaseTableComboBox.setGeometry(QtCore.QRect(10, 100, 131, 41))
        self.databaseTableComboBox.setObjectName("databaseTableComboBox")
        self.databaseTableComboBox.setVisible(False)
        self.databaseTableComboBox.currentIndexChanged.connect(self.select_table)

        self.resetButton = QtWidgets.QPushButton(self.centralwidget)
        self.resetButton.setEnabled(True)
        self.resetButton.setGeometry(QtCore.QRect(700, 100, 91, 41))
        self.resetButton.setObjectName("resetButton")
        self.resetButton.clicked.connect(self.reset_table)

        ###################################
        #           TABLE VIEW            #
        ###################################

        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(10, 150, 781, 391))
        self.tableView.setObjectName("tableView")

        ###################################
        #            MENU BAR             #
        ###################################

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")

        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")

        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.importAction = QtWidgets.QAction(MainWindow)
        self.importAction.setObjectName("importAction")
        self.importAction.triggered.connect(self.open_file_dialog)

        self.saveMenuAction = QtWidgets.QAction(MainWindow)
        self.saveMenuAction.setObjectName("saveMenuAction")
        self.saveMenuAction.triggered.connect(self.save_file_dialog)

        self.exitMenuAction = QtWidgets.QAction(MainWindow)
        self.exitMenuAction.setObjectName("exitMenuAction")
        self.exitMenuAction.triggered.connect(MainWindow.close)
        
        self.menu.addAction(self.importAction)
        self.menu.addSeparator()
        self.menu.addAction(self.saveMenuAction)
        self.menu.addAction(self.exitMenuAction)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        ###################################
        #            DATABASE             #
        ###################################

        self.db = None

        ###################################
        #             MODELS              #
        ###################################

        # Models are used to manage the data and the data is displayed using the TableView widget
        #
        # model is default set to None since there are two models that
        # can be used in the program. (QStandardItemModel and QSqlTableModel)

        # QSortFilterProxyModel allows for filtered data to be edited while maintaining the original model using a proxy model
        # The proxy model can be filtered and the data edited in the filtered table is reflected on the original model without
        # having to rewrite the whole model.
        self.model = None
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KLM Editor"))
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.saveButton.setText(_translate("MainWindow", "Save"))
        self.filterButton.setText(_translate("MainWindow", "Filter"))
        self.exitButton.setText(_translate("MainWindow", "Exit"))
        self.queryButton.setText(_translate("MainWindow", "Query"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        self.nameLabel.setText(_translate("MainWindow", "KLM Editor"))
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.importAction.setText(_translate("MainWindow", "Import"))
        self.saveMenuAction.setText(_translate("MainWindow", "Save"))
        self.exitMenuAction.setText(_translate("MainWindow", "Quit"))
    
    ################################################
    #                 FILE DIALOGS                 #
    ################################################

    def open_file_dialog(self):
        filename = QFileDialog.getOpenFileName(filter="CSV File (*.csv);;Database File (*.db)")
        split_filename = os.path.splitext(filename[0])

        file_name = split_filename[0]
        file_extension = split_filename[1]

        if filename:
            if file_extension == ".csv":
                with open(file_name + file_extension, newline='') as f:
                    # Disable database query related UI elements
                    self.filterButton.setVisible(True)
                    self.queryButton.setVisible(False)
                    self.databaseTableComboBox.setVisible(False)
                    self.inputLine.setGeometry(10, 100, 581, 41)
                    self.inputLine.clear()

                    # Close old connection and reset UI if connection exists
                    if self.db != None:
                        self.db.close()
                        self.reset_combobox()

                    # Load data from csv file into a list to be added to the model
                    reader = csv.reader(f)
                    data = list(reader)
                    data_header = list(data[0]) # for the header row
                    data.pop(0)
                    
                    # Creation of the base model and proxy model
                    self.model = QtGui.QStandardItemModel(len(data) - 1, len(data[0]))
                    self.model.setHorizontalHeaderLabels(data_header)
                    self.fill_model_from_data(data)
                    self.filter_proxy_model.setSourceModel(self.model)

                    # Model is displayed using the proxy model
                    self.tableView.setModel(self.filter_proxy_model)
                    self.reset_table()
            
            elif file_extension == ".db":
                # Disable csv related UI elements
                self.filterButton.setVisible(False)
                self.queryButton.setVisible(True)
                self.databaseTableComboBox.setVisible(True)
                self.inputLine.setGeometry(150, 100, 441, 41)
                self.inputLine.clear()

                # Close old connection and reset UI if connection exists
                if self.db != None:
                    self.db.close()
                    self.reset_combobox()

                self.db = QSqlDatabase.addDatabase("QSQLITE")
                self.db.setDatabaseName(file_name + file_extension)

                if self.db.open():
                    self.model = QSqlTableModel()

                    # First table in database is open and displayed by default
                    statement = "SELECT * FROM " + self.db.tables()[0]
                    query = QSqlQuery(statement)
                    self.populate_combobox(self.db)
                    self.model.setQuery(query)

                    self.tableView.setModel(self.model)

                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("Connection to database failed.")
                    msg.setInformativeText("Please try again.")
                    msg.setWindowTitle("Error")
                    msg.exec_()

    def save_file_dialog(self):
        if self.model != None:
            filename = QFileDialog.getSaveFileName(filter="CSV File (*.csv);;Database File (*.db)")
            split_filename = os.path.splitext(filename[0])

            file_name = split_filename[0]
            file_extension = split_filename[1]

            if file_extension == ".csv":
                self.export_model_to_csv(file_name, file_extension)
            elif file_extension == ".db":
                self.export_model_to_db(file_name, file_extension)
        
        # Prevent user from saving if no data is loaded
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Cannot save to file when no file is loaded.")
            msg.setInformativeText("Please open file and try again.")
            msg.setWindowTitle("Error")
            msg.exec_()

    def fill_model_from_data(self, data):
        for x in range(0, len(data)):
            for y in range(0, len(data[x])):
                item = QtGui.QStandardItem(data[x][y])
                self.model.setItem(x, y, item)

    ################################################
    #                    EXPORT                    #
    ################################################

    def export_model_to_csv(self, file_name, file_extension):
        if type(self.model) == type(QtGui.QStandardItemModel(0,0)):
            data = []
            row = []

            row_count = self.model.rowCount()
            column_count = self.model.columnCount()

            # Appending header row of the table
            for x in range(0, column_count):
                row.append(self.model.horizontalHeaderItem(x).text())
            
            data.append(row)
            row = []

            # Appending rest of the data rows in the table
            for x in range(0, row_count):
                for y in range(0, column_count):
                    row.append(self.model.item(x,y).text())
                
                data.append(row)
                row = []

            # Writing the nested list of data to a .csv spreadsheet
            with open(file_name + file_extension, 'w', newline='', encoding='utf-8') as f:
                wr = csv.writer(f)
                wr.writerows(data)
        
        elif type(self.model) == type(QSqlTableModel()):
            # The query shown in the Table View will be lost during the process of saving
            # Saving the original query will allow for the table to keep its original state after saving
            original_query = self.model.query()

            # Each table will be exported to its own csv file
            for table_num in range(0, len(self.db.tables())):
                data = []
                row = []

                row_count = self.model.rowCount()
                column_count = self.model.columnCount()

                table_name = self.db.tables()[table_num]

                query = QSqlQuery("SELECT * FROM " + self.db.tables()[table_num])
                self.model.setQuery(query)

                # Header
                for x in range(0, column_count):
                    row.append(self.model.headerData(x, QtCore.Qt.Horizontal))

                data.append(row)
                row = []

                # Data
                for x in range(0, row_count):
                    for y in range(0, column_count):
                        row.append(self.model.record(x).value(y))

                    data.append(row)
                    row = []

                # Saving current table to .csv
                with open(file_name + "_" + table_name + file_extension, 'w', newline='', encoding='utf-8') as f:
                    wr = csv.writer(f)
                    wr.writerows(data) 

            # Display the query that was shown before saving
            self.model.setQuery(original_query)

    def export_model_to_db(self, file_name, file_extension):
        # Similar to export_model_to_csv in retrieving information
        # Used both sqlite3 and pandas modules to export because sqlite3 makes it easier 
        # to write to a database file
        connection = sqlite3.connect(file_name + file_extension)

        if type(self.model) == type(QtGui.QStandardItemModel(0,0)):
            headers = []

            for x in range(0, self.model.columnCount()):
                headers.append(self.model.horizontalHeaderItem(x).text())

            data = []
            row = []

            for x in range(0, self.model.rowCount()):
                for y in range(0, self.model.columnCount()):
                    row.append(self.model.item(x,y).text())
                
                data.append(row)
                row = []
            
            df = pd.DataFrame(data, columns = headers)
            df.to_sql(QtCore.QFileInfo(file_name).fileName(), connection, if_exists='replace', index=False)

        elif type(self.model) == type(QSqlTableModel()):
            for t in range(0, len(self.db.tables())):
                headers = []
                data = []
                row = []

                query = QSqlQuery("SELECT * FROM " + self.db.tables()[t])
                self.model.setQuery(query)

                for x in range(0, self.model.columnCount()):
                    headers.append(self.model.headerData(x, QtCore.Qt.Horizontal))

                for x in range(0, self.model.rowCount()):
                    for y in range(0, self.model.columnCount()):
                        row.append(self.model.record(x).value(y))

                    data.append(row)
                    row = []
                
                df = pd.DataFrame(data, columns = headers)
                df.to_sql(self.db.tables()[t], connection, if_exists='replace', index=False)

        connection.close()

    ################################################
    #               UI MANIPULATION                #
    ################################################
    
    def populate_combobox(self, db):
        if type(self.model) == type(QSqlTableModel()):
            for x in range(0, len(db.tables())):
                self.databaseTableComboBox.addItem(db.tables()[x])

    def reset_combobox(self):
        self.databaseTableComboBox.clear()

    def select_table(self):
        current_index = self.databaseTableComboBox.currentIndex()

        if type(self.model) == type(QSqlTableModel()):
            # Default index of a QComboBox widget is -1
            # Set conditional so that it's not automatically called when filled
            if self.databaseTableComboBox.currentIndex() != -1:
                statement = "SELECT * FROM " + self.db.tables()[current_index]
                self.model.setTable(self.db.tables()[current_index])
                self.execute_query_from_statement(statement)

    def reset_table(self):
        self.inputLine.clear()
        
        if type(self.model) == type(QtGui.QStandardItemModel(0,0)):
            self.filter_proxy_model.setFilterKeyColumn(-1) # -1 selects all columns
            self.filter_proxy_model.setFilterRegExp("")    # Empty reg expression resets model

        elif type(self.model) == type(QSqlTableModel()):
            self.select_table()

    def filter_table(self):
        if type(self.model) == type(QtGui.QStandardItemModel(0,0)):
            # Split into: column name and filter value
            split_filter = self.inputLine.text().split('=')
            header_column = self.get_header_column(split_filter[0])

            if header_column != None:
                self.filter_proxy_model.setFilterKeyColumn(header_column)
                self.filter_proxy_model.setFilterRegExp(split_filter[1])

    def get_header_column(self, header_label):
        # Returns index of column specified in the filter
        for x in range(0, self.model.columnCount()):
            if header_label == self.model.horizontalHeaderItem(x).text():
                return x
        
        # User may input a column name that doesn't exist
        return None

    ################################################
    #               QUERY FUNCTIONS                #
    ################################################

    def execute_query_from_input_line(self):
        if type(self.model) == type(QSqlTableModel()):
            # Executes query from input line
            query = QSqlQuery(self.inputLine.text())
            self.model.setQuery(query)

    def execute_query_from_statement(self, statement):
        if type(self.model) == type(QSqlTableModel()):
            query = QSqlQuery(statement)
            self.model.setQuery(query)