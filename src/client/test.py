import sys
from PySide6.QtWidgets import (
    QApplication,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsRectItem,
)
from PySide6.QtCore import Qt

app = QApplication(sys.argv)

scene = QGraphicsScene()

rect = QGraphicsRectItem(0, 0, 100, 100)
rect.setFlag(QGraphicsRectItem.ItemIsMovable)  # Objekt bewegbar
rect.setFlag(QGraphicsRectItem.ItemIsSelectable)

scene.addItem(rect)

view = QGraphicsView(scene)
view.setRenderHint(view.renderHints())
view.resize(600, 400)
view.show()

sys.exit(app.exec())
