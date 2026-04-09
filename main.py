import sys
from PyQt6 import QtWidgets
from window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    m_window = MainWindow()

    sys.exit(app.exec())
