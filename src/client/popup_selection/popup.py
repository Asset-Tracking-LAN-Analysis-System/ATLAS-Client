import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QPushButton,
    QVBoxLayout,
    QInputDialog,
    QDialog,
    QListWidget,
    QListWidgetItem,
    QDialogButtonBox,
)
from PySide6.QtCore import Qt


class device_selection(QDialog):
    """Custom dialog for multiple selection."""

    def __init__(self, items, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Select Items")
        self.resize(300, 300)

        self.list_widget = QListWidget(self)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        for item in items:
            QListWidgetItem(item, self.list_widget)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self
        )

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addWidget(self.list_widget)
        layout.addWidget(self.button_box)

    def selected_items(self):
        return [item.text() for item in self.list_widget.selectedItems()]
