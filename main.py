#!/bin/env python

from mort import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
import sys


class RepayTable(QtCore.QAbstractTableModel):
    def __init__(self):
        super(RepayTable, self).__init__()
        self._headings = ['Principal', 'Capital', 'Interest','Total Interest']        

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignRight

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headings[col]
        return None

    def update(self, num_repayments, principal, int_rate):
        self._data = getGraphData(num_repayments, principal, int_rate)
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(None),
                                               self.columnCount(None)))

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(Ui, self).__init__()
        uic.loadUi('mort.ui', self)  # Load the .ui file
        self.show()  # Show the GUI

        # collect all the Ui pointers we need to interact with GUI
        self.btnCalc = self.findChild(QtWidgets.QPushButton, 'btnCalc')
        self.principal = self.findChild(QtWidgets.QSpinBox, 'principal')
        self.interest = self.findChild(QtWidgets.QDoubleSpinBox, 'interest')
        self.years = self.findChild(QtWidgets.QSpinBox, 'years')
        self.textOutput = self.findChild(QtWidgets.QTextEdit, 'output')
        self.table = self.findChild(QtWidgets.QTableView, 'tableView')

        #set up model for the table
        self.model = RepayTable()        
        self.model.update(self.years.value()*12,
                          self.principal.value(),
                          self.interest.value())
        self.table.setModel(self.model)

        # connect GUI elements to functions
        self.btnCalc.clicked.connect(self.calculate)

    def calculate(self):
        interest = self.interest.value()
        principal = self.principal.value()
        years = self.years.value()

        self.textOutput.clear()
        self.textOutput.append("Interest Rate: {0:.2f}%".format(interest))
        self.textOutput.append("Principal: £" + str(principal))
        self.textOutput.append("Years: " + str(years))

        repayment = calcRepayment(12 * years, principal, interest)

        self.textOutput.append("Repyament: £" + str(repayment) + " per month")
        self.model.update(years * 12, principal, interest)


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
