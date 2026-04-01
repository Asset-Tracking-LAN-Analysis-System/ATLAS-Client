
import sys
import json
import requests
from difflib import SequenceMatcher

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QTableView,
    QPushButton,
    QLabel,
    QFrame,
    QLineEdit,
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSortFilterProxyModel


class FuzzyFilterProxyModel(QSortFilterProxyModel):
    def __init__(self):
        super().__init__()
        self.query = ""

    def setFilterText(self, text):
        self.query = text.lower()
        self.invalidateFilter()

    def fuzzy_match(self, text, query):
        if not query:
            return True

        text = text.lower()

        if query in text:
            return True

        ratio = SequenceMatcher(None, query, text).ratio()
        return ratio > 0.5

    def filterAcceptsRow(self, source_row, source_parent):
        if not self.query:
            return True

        model = self.sourceModel()

        for col in range(model.columnCount()):
            index = model.index(source_row, col, source_parent)
            data = str(model.data(index))

            if self.fuzzy_match(data, self.query):
                return True

        return False
