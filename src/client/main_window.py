from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableView, QPushButton, QLabel, QFrame, QLineEdit, QMenu
)
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtCore import Qt, QSettings

from data_handler.api_handler import api_handler
from filters.fuzzyfilter import FuzzyFilterProxyModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ATLAS Client")
        self.resize(1000, 600)

        self.db = api_handler()
        self.setStyleSheet(self.dark_style())

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)

        sidebar = self.create_sidebar()
        content = self.create_content()

        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        self.setCentralWidget(main_widget)

        self.load_data()

        self.header = self.table.horizontalHeader()
        self.header.setContextMenuPolicy(Qt.CustomContextMenu)
        self.header.customContextMenuRequested.connect(self.show_header_menu)

    # ---------- TABLE STATE ----------

    def save_table_state(self):
        settings = QSettings("MyApp", "AtlasClient")
        settings.setValue("header_state", self.header.saveState())

    def load_table_state(self):
        settings = QSettings("MyApp", "AtlasClient")
        state = settings.value("header_state")
        if state:
            self.header.restoreState(state)

    def closeEvent(self, event):
        self.save_table_state()
        super().closeEvent(event)

    # ---------- HEADER MENU ----------

    def show_header_menu(self, pos):
        menu = QMenu(self)

        for i, attr in enumerate(self.ATTRIBUTES):
            action = menu.addAction(attr)
            action.setCheckable(True)
            action.setChecked(not self.table.isColumnHidden(i))

            action.triggered.connect(
                lambda checked, col=i: self.toggle_column(col, checked)
            )

        menu.exec(self.header.mapToGlobal(pos))

    def toggle_column(self, column, visible):
        self.table.setColumnHidden(column, not visible)

    # ---------- UI ----------

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

    # ---------- DATA ----------

    def load_data(self):
        data = self.db.fetch_data()

        self.ATTRIBUTES = ["ID", "NAME", "Status", "IP"]

        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(self.ATTRIBUTES)

        for entity in data["data"]:
            items = [QStandardItem(str(entity.get(attr, ""))) for attr in self.ATTRIBUTES]
            self.model.appendRow(items)

        self.proxy = FuzzyFilterProxyModel()
        self.proxy.setSourceModel(self.model)

        self.table.setModel(self.proxy)

        self.header = self.table.horizontalHeader()
        self.header.setStretchLastSection(True)
        self.header.setSectionsMovable(True)  # drag columns

        self.load_table_state()

    def on_search(self, text):
        self.proxy.setFilterText(text)

    # ---------- STYLE ----------

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