from mort import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt

class RepayTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(RepayTableModel, self).__init__()
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
        
