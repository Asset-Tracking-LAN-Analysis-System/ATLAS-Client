import sys
from PySide6.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PySide6.QtGui import QPen
from PySide6.QtCore import Qt, QTimer
from .widget import CanvasIcon


from popup_selection.popup import device_selection


class Canvas(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 800, 500)
        self.setScene(self.scene)
        self.icons = []
        self.setFixedSize(800, 500)

        # Beispiel-Icons
        self.add_icon("icon.png", 50, 50)
        self.add_icon("icon.png", 200, 100)

        # Linie als Attribut speichern, damit wir sie jedes Mal aktualisieren können
        self.line = None

        # Timer einrichten
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_line)
        self.timer.start(30)  # 30 ms ≈ 33 FPS

    def add_icon(self, path, x, y):
        icon = CanvasIcon(path, x, y)
        self.icons.append(icon)
        self.scene.addItem(icon)

    def draw_line(self, x1, y1, x2, y2):
        pen = QPen(Qt.black)
        pen.setWidth(2)

        # Wenn Linie schon existiert, löschen wir sie zuerst
        if self.line:
            self.scene.removeItem(self.line)

        self.line = self.scene.addLine(x1, y1, x2, y2, pen)

    def update_line(self):
        if len(self.icons) >= 2:
            # Linie zwischen den Mittelpunkten der Icons
            size = CanvasIcon.SIZE
            x1 = self.icons[0].pos().x() + size / 2
            y1 = self.icons[0].pos().y() + size / 2
            x2 = self.icons[1].pos().x() + size / 2
            y2 = self.icons[1].pos().y() + size / 2
            self.draw_line(x1, y1, x2, y2)

    def wheelEvent(self, event):
        # Delta des Mausrads
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print("Right mouse button was clicked")

            dialog = device_selection(items=["Test1", "Test2", "Test3"], parent=self)

            if dialog.exec():
                print(dialog.selected_items())

        elif event.button() == Qt.LeftButton:
            print("Left mouse button pressed")

        return super().mousePressEvent(event)
