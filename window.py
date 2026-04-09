from PyQt6.QtWidgets import QMainWindow, QMdiArea, QMdiSubWindow, QPushButton
from app import AppWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        #self.setWindowTitle("Linus")
        widget = AppWidget()
        widget.resize(800, 600)
        widget.show()

        mdi_area = QMdiArea()
        self.setCentralWidget(mdi_area)

        sub = QMdiSubWindow()
        sub.setWidget(QPushButton())
        sub.setWindowTitle("trthbtr")
        mdi_area.addSubWindow(sub)
        sub.show()





