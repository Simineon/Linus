import sys
import os
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent, QAction
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QTabWidget, QVBoxLayout, QDialog, QSplitter, QFrame, \
    QLabel


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.lay = QVBoxLayout(self)
        self.menuBar = QMenuBar()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.setupTab()

        self.setupExplorer()

        self.splitter.addWidget(self.tab)
        self.splitter.setSizes([200, 600])

        self.lay.addWidget(self.splitter)

        self.setupMenu()
        self.new_tab()

        self.setupStyle()

    def setupStyle(self):
        with open("static/style.qss", encoding="utf-8") as st_file:
            self.setStyleSheet(st_file.read())

    def setupMenu(self):
        self.fileMenu = self.menuBar.addMenu("&File")

        self.newFile = QAction("New file", self)
        self.newFile.setShortcut("Ctrl+T")
        self.newFile.triggered.connect(self.new_tab)

        self.close_tab_action = QAction("Close Tab", self)
        self.close_tab_action.setShortcut("Ctrl+W")
        self.close_tab_action.triggered.connect(self.close_tab)

        self.fileMenu.addAction(self.close_tab_action)

        self.fileMenu.addAction(self.newFile)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Exit", self.close)

        self.lay.setMenuBar(self.menuBar)

    def setupTab(self):
        self.tab = QTabWidget()
        self.tab.setMovable(True)
        self.tab.setTabsClosable(True)
        self.tab.tabCloseRequested.connect(self.close_tab)

    def new_tab(self):
        tab_inside = QWidget()
        tab_lay = QVBoxLayout(tab_inside)
        tab_lay.setContentsMargins(0, 0, 0, 0)

        te = CustomTextEdit()
        tab_lay.addWidget(te)

        tab_index = self.tab.addTab(tab_inside, "Untitled")
        self.tab.setCurrentIndex(tab_index)

        print("Tab AMOOOONG UUSSSS")

    def close_tab(self, index):
        self.tab.removeTab(index)

    def setupExplorer(self):
        self.explorer_frame = QFrame()
        self.explorer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.explorer_frame.setMinimumWidth(150)

        explorer_layout = QVBoxLayout(self.explorer_frame)
        explorer_layout.setContentsMargins(0, 0, 0, 0)

        self.explorerLabel = QLabel("Directory's Explorer")
        self.explorerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        explorer_layout.addWidget(self.explorerLabel)

        self.splitter.addWidget(self.explorer_frame)
        #self.explorer = QDialog()


class CustomTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Tab:
            self.insertPlainText("    ")
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = AppWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())