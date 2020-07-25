from pathlib import Path

import pandas as pd

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog, QDesktopWidget


class TableModel(QAbstractTableModel):
    def __init__(self, df=pd.DataFrame(), parent=None):
        QAbstractTableModel.__init__(self, parent)
        self.df = df

    def sort(self, p_int, order=None):
        # Storing persistent indexes
        self.layoutAboutToBeChanged.emit()
        oldIndexList = self.persistentIndexList()
        oldIds = self.df.index.copy()

        # Sorting data
        column = self.df.columns[p_int]
        ascending = (order == Qt.AscendingOrder)
        self.df = self.df.sort_values(by=column, ascending=ascending)

        # Updating persistent indexes
        newIds = self.df.index
        newIndexList = []
        for index in oldIndexList:
            id = oldIds[index.row()]
            newRow = newIds.get_loc(id)
            newIndexList.append(self.index(newRow, index.column(), index.parent()))
        self.changePersistentIndexList(oldIndexList, newIndexList)
        self.layoutChanged.emit()
        self.dataChanged.emit(QModelIndex(), QModelIndex())

    def rowCount(self, parent):
        return len(self.df)

    def columnCount(self, parent):
        return len(self.df.columns)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif (role == Qt.BackgroundRole):
            mapper = {
                'YES': Qt.green,
                'NO': Qt.red,
                'N/A': Qt.lightGray
            }
            retval = mapper.get(self.df.values[index.row(), index.column()])
            if retval is not None:
                return QBrush(retval)
            else:
                return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.df.values[index.row(), index.column()])

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.df.columns[col])
        return QVariant()


class TableWindow(QtWidgets.QMainWindow):
    def __init__(self, df):
        super().__init__()
        uic.loadUi(Path(__file__).parent/'table.ui', self)
        self.setWindowTitle('Phenotrex Results')
        # ag = QDesktopWidget().availableGeometry()
        # self.setMaximumHeight(ag.height())
        # self.setMaximumWidth(ag.width())
        self.df = df
        self.display_df = self.get_masked_df()
        self.tableView.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.confidenceCutoffSpinBox.valueChanged.connect(self.update_table_after_spinner)
        self.saveButton.clicked.connect(self.save_df)
        self.recalculate_table()

    def get_masked_df(self, conf_co: float = 0.5):
        df = self.df.copy()
        df.loc[df['Confidence'].astype(float) < conf_co, 'Trait Present'] = 'N/A'
        return df

    def recalculate_table(self):
        self.model = TableModel(
            df=self.display_df,
        )
        self.tableView.setModel(self.model)
        self.tableView.resizeColumnsToContents()
        self.tableView.update()

    def update_table_after_spinner(self):
        self.display_df = self.get_masked_df(conf_co=float(self.confidenceCutoffSpinBox.value()))
        self.recalculate_table()

    def save_df(self):
        outpath = QFileDialog.getSaveFileName(self, 'Save File', str(Path.home()))[0]
        self.display_df.to_csv(outpath, sep='\t', index=None)
