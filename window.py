from PyQt6.QtWidgets import QMainWindow, QMdiArea, QMdiSubWindow
from app import AppWidget
from terminal_emulator import TerminalWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        widget = AppWidget()
        widget.resize(800, 600)
        widget.show()

        mdi = QMdiArea()
        terminal_window = QMdiSubWindow()
        term_widget = TerminalWidget()
        terminal_window.setWidget(term_widget)
        mdi.addSubWindow(terminal_window)
        terminal_window.show()


        self.setCentralWidget(mdi)
