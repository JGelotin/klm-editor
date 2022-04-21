import sys
import os
import csv
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
        self.queryButton.clicked.connect(self.execute_query)
        
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

                self.db = QSqlDatabase.addDatabase("QSQLITE")
                self.db.setDatabaseName(file_name + file_extension)

                if self.db.open():
                    self.model = QSqlTableModel()

                    # First table in database is open and displayed by default
                    statement = "SELECT * FROM " + self.db.tables()[0]
                    query = QSqlQuery(statement)
                    self.model.setQuery(query)

                    self.tableView.setModel(self.model)

    def execute_query(self):
        if type(self.model) == type(QSqlTableModel()):
            # Executes query from input line
            query = QSqlQuery(self.inputLine.text())
            self.model.setQuery(query)

    def execute_query(self, statement):
        if type(self.model) == type(QSqlTableModel()):
            query = QSqlQuery(statement)
            self.model.setQuery(query)

    def fill_model_from_text(self, data):
        for x in range(0, len(data)):
            for y in range(0, len(data[x])):
                item = QtGui.QStandardItem(data[x][y])
                self.model.setItem(x, y, item)

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