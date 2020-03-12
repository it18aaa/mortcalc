#!/bin/env python

from mort import *
from PyQt5 import QtWidgets, uic, QtCore, Qt
import sys

class repaymentsTable(QtCore.QAbstractTableModel):
    def rowcount(self, data):
        return 300

    def columnCount(self, data):
        return 4

    def data(self, index):
        return 4

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
        graphData = getGraphData(12 * years, principal, interest)

        self.textOutput.append("Repyament: £" + str(repayment) + " per month")


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
