from moveable_widgets.canva import Canvas
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    canvas = Canvas()
    canvas.show()

    sys.exit(app.exec())
