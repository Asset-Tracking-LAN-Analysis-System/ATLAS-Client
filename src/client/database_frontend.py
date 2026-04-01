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


class Database:
    def __init__(self):
        with open("client/config.json", "r") as config_file:
            config = json.load(config_file)
        self.api_url = f"{str(config['api_url'])}:{str(config['api_port'])}"
        print(f"Connecting to {self.api_url}")

    def fetch_data(self):

        response = requests.get(url=self.api_url + "/entities")
        data = response.json()

        return data


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATLAS Client")
        self.resize(1000, 600)

        self.db = Database()

        self.setStyleSheet(self.dark_style())

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        sidebar = self.create_sidebar()
        content = self.create_content()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.setCentralWidget(main_widget)

        self.load_data()

    def create_sidebar(self):
        frame = QFrame()
        frame.setFixedWidth(200)
        layout = QVBoxLayout(frame)

        title = QLabel("ATLAS")
        title.setObjectName("title")

        btn_devices = QPushButton("Devices")
        btn_users = QPushButton("Users")

        layout.addWidget(title)
        layout.addSpacing(20)
        layout.addWidget(btn_devices)
        layout.addWidget(btn_users)
        layout.addStretch()

        return frame

    def create_content(self):
        frame = QFrame()
        layout = QVBoxLayout(frame)

        toolbar = QHBoxLayout()
        self.search = QLineEdit()
        self.search.setPlaceholderText("Suchen...")
        self.search.textChanged.connect(self.on_search)

        refresh_btn = QPushButton("Aktualisieren")

        toolbar.addWidget(self.search)
        toolbar.addWidget(refresh_btn)

        self.table = QTableView()

        layout.addLayout(toolbar)
        layout.addWidget(self.table)

        return frame

    def load_data(self):
        data = self.db.fetch_data()

        ATTRIBUTES = ["ID", "NAME", "Status", "IP"]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(ATTRIBUTES)

        print(data)
        for entity in data["data"]:
            items = [QStandardItem(str(entity.get(attr, ""))) for attr in ATTRIBUTES]
            self.model.appendRow(items)

        self.proxy = FuzzyFilterProxyModel()
        self.proxy.setSourceModel(self.model)

        self.table.setModel(self.proxy)
        self.table.horizontalHeader().setStretchLastSection(True)

    def on_search(self, text):
        self.proxy.setFilterText(text)

    def dark_style(self):
        return """
        QWidget {
            background-color: #0f172a;
            color: #e2e8f0;
            font-family: Segoe UI;
            font-size: 14px;
        }

        QFrame {
            background-color: #020617;
        }

        QLabel#title {
            font-size: 20px;
            font-weight: bold;
            color: #3b82f6;
        }

        QPushButton {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 6px;
            border-radius: 6px;
        }

        QPushButton:hover {
            background-color: #3b82f6;
        }

        QLineEdit {
            background-color: #020617;
            border: 1px solid #334155;
            padding: 6px;
            border-radius: 6px;
        }

        QTableView {
            background-color: #020617;
            gridline-color: #1e293b;
            border: 1px solid #334155;
        }

        QHeaderView::section {
            background-color: #1e293b;
            padding: 5px;
            border: none;
        }
        """


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
