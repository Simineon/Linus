import sys
import os
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDir, QModelIndex, QRect
from PyQt6.QtGui import QKeyEvent, QAction, QFileSystemModel, QPainter, QColor, QTextFormat
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QTabWidget, QVBoxLayout, QDialog, QSplitter, QFrame, \
    QLabel, QFileDialog, QTreeView, QPushButton, QTextEdit


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
        self.splitter.setSizes([300, 500])

        self.lay.addWidget(self.splitter)

        self.setupMenu()
        self.new_tab()

        self.setupStyle()

    def setupStyle(self):
        try:
            with open("static/style.qss", encoding="utf-8") as st_file:
                self.setStyleSheet(st_file.read())
        except FileNotFoundError:
            print("Style file not found, using default style")

    def setupMenu(self):
        self.fileMenu = self.menuBar.addMenu("&File")

        self.newFile = QAction("New file", self)
        self.newFile.setShortcut("Ctrl+T")
        self.newFile.triggered.connect(self.new_tab)

        self.close_tab_action = QAction("Close Tab", self)
        self.close_tab_action.setShortcut("Ctrl+W")
        self.close_tab_action.triggered.connect(self.close_current_tab)

        self.open_action = QAction("Open", self)

        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.openFile)

        self.open_folder_action = QAction("Open Folder", self)
        self.open_folder_action.setShortcut("Ctrl+Shift+O")
        self.open_folder_action.triggered.connect(self.openFolder)

        self.fileMenu.addAction(self.newFile)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.open_folder_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.close_tab_action)
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

        self.te = CustomTextEdit()
        tab_lay.addWidget(self.te)

        tab_index = self.tab.addTab(tab_inside, "Untitled")
        self.tab.setCurrentIndex(tab_index)

        print("Tab AMOOOONG UUSSSS")

    def close_tab(self, index):
        self.tab.removeTab(index)

    def close_current_tab(self):
        current_index = self.tab.currentIndex()
        if current_index >= 0:
            self.tab.removeTab(current_index)

    def setupExplorer(self):
        self.explorer_frame = QFrame()
        self.explorer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.explorer_frame.setMinimumWidth(200)

        explorer_layout = QVBoxLayout(self.explorer_frame)
        explorer_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        self.explorerLabel = QLabel("Directory")
        self.explorerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.directory_button = QPushButton("Select Directory")
        self.directory_button.clicked.connect(self.openFolder)

        header_layout.addWidget(self.explorerLabel)
        header_layout.addWidget(self.directory_button)
        explorer_layout.addLayout(header_layout)

        self.file_model = QFileSystemModel()
        self.file_model.setRootPath(QDir.rootPath())
        self.file_model.setFilter(QDir.Filter.NoDotAndDotDot | QDir.Filter.AllEntries)

        self.file_tree = QTreeView()
        self.file_tree.setModel(self.file_model)
        self.file_tree.setAnimated(True)
        self.file_tree.setIndentation(20)
        self.file_tree.setSortingEnabled(True)

        self.file_tree.setHeaderHidden(True)
        self.file_tree.hideColumn(1)
        self.file_tree.hideColumn(2)
        self.file_tree.hideColumn(3)

        self.file_tree.doubleClicked.connect(self.on_file_double_click)

        explorer_layout.addWidget(self.file_tree)

        self.splitter.addWidget(self.explorer_frame)

    def openFolder(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            QDir.homePath(),
            QFileDialog.Option.ShowDirsOnly
        )

        if folder_path:
            index = self.file_model.setRootPath(folder_path)
            self.file_tree.setRootIndex(index)

            self.explorerLabel.setText(f"Folder: {os.path.basename(folder_path)}")

            self.file_tree.expand(index)

            print(f"Opened folder: {folder_path}")

    def on_file_double_click(self, index: QModelIndex):
        file_path = self.file_model.filePath(index)
        file_info = self.file_model.fileInfo(index)

        if file_info.isDir():
            self.file_tree.setRootIndex(index)
            self.explorerLabel.setText(f"Folder: {file_info.fileName()}")
        else:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    current_widget = self.tab.currentWidget()
                    if current_widget:
                        te = current_widget.findChild(CustomTextEdit)
                        if te:
                            te.setPlainText(content)
                            current_index = self.tab.currentIndex()
                            self.tab.setTabText(current_index, os.path.basename(file_path))
            except Exception as e:
                print(f"Error reading file: {e}")

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory=QDir.homePath()
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    self.data = file.read()
                    current_widget = self.tab.currentWidget()
                    if current_widget:
                        te = current_widget.findChild(CustomTextEdit)
                        te.setPlainText(self.data)

                        current_index = self.tab.currentIndex()
                        self.tab.setTabText(current_index, os.path.basename(file_path))
            except Exception as e:
                print(f"Error reading file: {e}")


class CustomTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.setPlainText("")

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(),
                                              self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        mypainter = QPainter(self.lineNumberArea)

        mypainter.fillRect(event.rect(), QColor(Qt.GlobalColor.lightGray))

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                mypainter.setPen(QColor(Qt.GlobalColor.black))
                mypainter.drawText(0, int(top), self.lineNumberArea.width(), height,
                                   Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.GlobalColor.yellow).lighter(160)
            selection.format.setBackground(lineColor)

            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()

            extraSelections.append(selection)

        self.setExtraSelections(extraSelections)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == QtCore.Qt.Key.Key_Tab:
            self.insertPlainText("    ")
        else:
            super().keyPressEvent(event)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QtCore.QSize(self.myeditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = AppWidget()
    widget.resize(800, 600)
    widget.show()

    sys.exit(app.exec())