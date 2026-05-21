from PyQt6.QtCore import Qt, QDir, QModelIndex
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QVBoxLayout, QSplitter, QFrame, \
    QLabel, QFileDialog, QTreeView, QPushButton, QLineEdit
from tab import Tab, CustomTextEdit
from runner import Runner

class TerminalWidgetAsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setWindowTitle("Terminal")

    def setup(self):
        self.lay = QVBoxLayout(self)

        self.tab = Tab(self)
        self.input = QLineEdit()
        self.button = QPushButton("Change position")

        self.lay.addWidget(self.input)
        self.lay.addWidget(self.button)
        self.lay.addWidget(self.tab.get_widget())

        self.tab.new_tab()

        self.setupStyle()

    def setupStyle(self):
        try:
            with open("static/style.qss", encoding="utf-8") as st_file:
                self.setStyleSheet(st_file.read())
        except FileNotFoundError:
            print("Style file not found, using default static")

    # на будущее
    def closeEvent(self, event):
        pass

class TerminalWidgetInWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.lay = QVBoxLayout(self)

        self.tab = Tab(self)
        self.label = QLabel("Terminal")
        self.button = QPushButton("Change position")

        self.lay.addWidget(self.label)
        self.lay.addWidget(self.button)
        self.lay.addWidget(self.tab.get_widget())

        self.tab.new_tab()

        #self.button.pressed(self.change_position)

        self.setupStyle()

    def change_position(self):
        print("sdsakdsakdnsajdn")

    def setupStyle(self):
        try:
            with open("static/style.qss", encoding="utf-8") as st_file:
                self.setStyleSheet(st_file.read())
        except FileNotFoundError:
            print("Style file not found, using default static")
