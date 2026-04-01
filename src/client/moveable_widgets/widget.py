from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class CanvasIcon(QGraphicsPixmapItem):
    SIZE = 64

    def __init__(self, image_path, x=0, y=0):
        super().__init__()

        pixmap = QPixmap(image_path).scaled(
            self.SIZE, self.SIZE, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        self.setPixmap(pixmap)
        self.setPos(x, y)

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)  # wichtig!

        self.x_coordinate = x
        self.y_coordinate = y

    def itemChange(self, change, value):

        if change == QGraphicsItem.ItemPositionChange and self.scene():
            rect = self.scene().sceneRect()

            x = value.x()
            y = value.y()

            x = max(rect.left(), min(x, rect.right() - self.SIZE))
            y = max(rect.top(), min(y, rect.bottom() - self.SIZE))

            return value.__class__(x, y)

        return super().itemChange(change, value)
