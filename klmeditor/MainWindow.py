import sys
import os
import csv
import sqlite3
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi("ui/MainWindow.ui", self)        
        self.queryButton.setVisible(False)
        self.databaseTableComboBox.setVisible(False)
        self.show()

        # Database
        self.db = None

        # Models are used to manage the data and the data is displayed using the TableView widget
        #
        # model is default set to None since there are two models that
        # can be used in the program. (QStandardItemModel and QSqlTableModel)

        # QSortFilterProxyModel allows for filtered data to be edited while maintaining the original model using a proxy model
        # The proxy model can be filtered and the data edited in the filtered table is reflected on the original model without
        # having to rewrite the whole model.
        self.model = None
        self.filter_proxy_model = QtCore.QSortFilterProxyModel()

        # Button Click Functions
        self.openButton.clicked.connect(self.open_file_dialog)
        self.exitButton.clicked.connect(self.close)
        self.filterButton.clicked.connect(self.filter_table)
        self.queryButton.clicked.connect(self.execute_query_from_input_line)
        self.resetButton.clicked.connect(self.reset_table)
        self.saveButton.clicked.connect(self.save_file_dialog)

        # Combo Box Functions
        self.databaseTableComboBox.currentIndexChanged.connect(self.select_table)

        # Menu Bar Action Functions
        self.importAction.triggered.connect(self.open_file_dialog)
        self.saveMenuAction.triggered.connect(self.save_file_dialog)
        self.exitMenuAction.triggered.connect(self.close)

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
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

                    # Load data from csv file into a list to be added to the model
                    reader = csv.reader(f)
                    data = list(reader)
                    data_header = list(data[0]) # for the header row
                    data.pop(0)
                    
                    # Creation of the base model and proxy model
                    self.model = QtGui.QStandardItemModel(len(data) - 1, len(data[0]))
                    self.model.setHorizontalHeaderLabels(data_header)
                    self.fill_model_from_text(data)
                    self.filter_proxy_model.setSourceModel(self.model)

                    # Model is displayed using the proxy model
                    self.tableView.setModel(self.filter_proxy_model)
            
            elif file_extension == ".db":
                # Disable csv related UI elements
                self.filterButton.setVisible(False)
                self.queryButton.setVisible(True)
                self.databaseTableComboBox.setVisible(True)
                self.inputLine.setGeometry(150, 100, 441, 41)
                self.inputLine.clear()

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

    def execute_query_from_input_line(self):
        if type(self.model) == type(QSqlTableModel()):
            # Executes query from input line
            query = QSqlQuery(self.inputLine.text())
            self.model.setQuery(query)

    def execute_query_from_statement(self, statement):
        if type(self.model) == type(QSqlTableModel()):
            query = QSqlQuery(statement)
            self.model.setQuery(query)

    def fill_model_from_text(self, data):
        for x in range(0, len(data)):
            for y in range(0, len(data[x])):
                item = QtGui.QStandardItem(data[x][y])
                self.model.setItem(x, y, item)

    def save_file_dialog(self):
        filename = QFileDialog.getSaveFileName(filter="CSV File (*.csv);;Database File (*.db)")
        split_filename = os.path.splitext(filename[0])

        file_name = split_filename[0]
        file_extension = split_filename[1]

        if file_extension == ".csv":
            self.export_model_to_csv(file_name, file_extension)
        elif file_extension == ".db":
            self.export_model_to_db(file_name, file_extension)

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
        # Similar to export_model_to_csv in retrieving information so just copied format
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

    def filter_table(self):
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    sys.exit(app.exec_())