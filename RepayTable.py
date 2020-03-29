from mort import *
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import Qt

class RepayTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super(RepayTableModel, self).__init__()
        self._headings = ['Payment', 'Month', 'Principal', 'Capital', 'Interest','Total Interest', 'payment']                        

    def setStartData(self, date):
        self.startDate = date

    def data(self, index, role):
        # if display role :-
        if role == Qt.DisplayRole:            
            #format the columns
            if(index.column() >= 2):
                return "£ {0:,.2f}".format( self._data[index.row()][index.column()]  )
            else:
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

    def update(self, num_repayments, principal, int_rate, start_date):
        # bit of a hack so that the view resizes to fit the data set
        self.beginResetModel()
        self._data = getGraphData(num_repayments, principal, int_rate, start_date)
        self.endResetModel()
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(None),
                                               self.columnCount(None)))

        
        
