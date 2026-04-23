from PyQt6.QtCore import Qt, QDir, QModelIndex
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QVBoxLayout, QSplitter, QFrame, \
    QLabel, QFileDialog, QTreeView, QPushButton
from tab import Tab, CustomTextEdit
from runner import Runner

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setWindowTitle("Terminal")

    def setup(self):
        self.lay = QVBoxLayout(self)

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.tab = Tab(self)

        self.splitter.addWidget(self.tab.get_widget())
        self.splitter.setSizes([300, 500])

        self.lay.addWidget(self.splitter)

        self.tab.new_tab()

        self.setupStyle()


    def set_output_text_in_widget(self, data):
        print(data)

    def setupStyle(self):
        try:
            with open("static/style.qss", encoding="utf-8") as st_file:
                self.setStyleSheet(st_file.read())
        except FileNotFoundError:
            print("Style file not found, using default static")

    # на будущее
    def closeEvent(self, event):
        pass

