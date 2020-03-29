#!/bin/env python


import matplotlib
from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from mort import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt
import sys
from RepayTable import RepayTableModel

import matplotlib
matplotlib.use('QT5Agg')


class Ui(QtWidgets.QMainWindow):
    def initVars(self):
        # collect all the Ui pointers we need to interact with GUI
        self.btnCalc = self.findChild(QtWidgets.QPushButton, 'btnCalc')
        self.principal = self.findChild(QtWidgets.QSpinBox, 'principal')
        self.interest = self.findChild(QtWidgets.QDoubleSpinBox, 'interest')
        self.years = self.findChild(QtWidgets.QSpinBox, 'years')
        self.textOutput = self.findChild(QtWidgets.QTextEdit, 'output')
        self.actionExit = self.findChild(QtWidgets.QAction, 'actionExit')
        self.table = self.findChild(QtWidgets.QTableView, 'tableView')
        self.graphWidget = self.findChild(QtWidgets.QWidget, 'graphWidget')

    def initTable(self):
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents)

        # set up model for the table
        self.model = RepayTableModel()
        self.model.update(self.years.value()*12,
                          self.principal.value(),
                          self.interest.value())
                          
        self.table.setModel(self.model)



    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mort.ui', self)
        self.initVars()
        self.initTable()
        self.initGraph()
    
        # connect GUI elements to functions
        self.btnCalc.clicked.connect(self.calculate)
        self.actionExit.triggered.connect(self.doQuit)

        self.principal.valueChanged.connect(self.calculate)
        self.interest.valueChanged.connect(self.calculate)
        self.years.valueChanged.connect(self.calculate)


        #update the graph
        self.calculate()

    def initGraph(self):
        # embed matplotlib canvas
        self.figure = Figure()
        self.graphCanvas = FigureCanvas(self.figure)        

        layout = QtWidgets.QVBoxLayout(self.graphWidget)            
        layout.addWidget(self.graphCanvas)
        self.graphCanvas.setParent(self.graphWidget)                   

        self.addToolBar(QtCore.Qt.BottomToolBarArea,
                        NavigationToolbar(self.graphCanvas, self))

        self._ax = self.graphCanvas.figure.subplots()
        self._ax.set_title('Mortgage repayment')
      
        # TODO : take into consideration DPI
        plt.rcParams.update({'font.size': 8})
        

    def calculate(self):
        interest = self.interest.value()
        principal = self.principal.value()
        years = self.years.value()

        self.textOutput.clear()
        self.textOutput.append("Principal: £" + str(principal))
       
        repayment = calcRepayment(12 * years, principal, interest)

        self.textOutput.append("Repyament: £" + str(repayment) + " per month")
        self.model.update(years * 12, principal, interest)
        
        self.updateGraph( years, principal, interest)
        

    def updateGraph(self, years, principal, interest):

        graphData = getGraphData(12*years, principal, interest)

        owed = list()
        running_total_int = list()
        running_total_cap = list()
        running_total_all = list()
        owed.append(principal)
        running_total_cap.append(0)
        running_total_int.append(0)
        running_total_all.append(0)

        totint = 0
        totcap = 0

        for month in graphData:

            # print("{0} £{1} £{2} £{3}".format(
            #     month[0], month[1], month[2], month[3]))

            totint += month[1]
            totcap += month[2]
            # if int(month.get("number")) % 12 == 0:
            owed.append(month[0])
            running_total_cap.append(totcap)
            running_total_int.append(totint)
            running_total_all.append(totcap + totint)

        self._ax.clear()
        self._ax.plot(owed, 'r-', label="Principal")
        self._ax.plot(running_total_int, 'b', label="Total Interest")
        self._ax.plot(running_total_cap, 'g', label="Total capital")
        self._ax.plot(running_total_all, 'y--', label="Running Total")
        self._ax.legend(loc="upper left")
        self._ax.grid(True, which='both')
        plt.minorticks_on()

        formatter = ticker.StrMethodFormatter('£{x:,.0f}')
        self._ax.yaxis.set_major_formatter(formatter)
        
        for tick in self._ax.yaxis.get_major_ticks():
            tick.label1.set_visible(True)
            tick.label2.set_visible(True)
            tick.label2.set_color('green')

        self._ax.set_ylabel('Amount')   
        self._ax.set_xlabel('Repayment')

        self._ax.figure.canvas.draw()

    def doQuit(self):
        print("Quit menu option selected")
        QtWidgets.QApplication.quit()


app = QtWidgets.QApplication(sys.argv)
window = Ui()
window.show()
app.exec_()
