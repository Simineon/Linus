import os
from winreg import HKEY_USERS

from PyQt6 import QtWidgets, QtCore
from PyQt6.QtCore import Qt, QDir, QModelIndex, QRect
from PyQt6.QtGui import QKeyEvent, QAction, QFileSystemModel, QPainter, QColor, QTextFormat
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QTabWidget, QVBoxLayout, QDialog, QSplitter, QFrame, \
    QLabel, QFileDialog, QTreeView, QPushButton, QTextEdit


class TabInfo:
    def __init__(self, widget, text_edit, file_path=None, is_saved=True):
        self.widget = widget
        self.text_edit = text_edit
        self.file_path = file_path
        self.is_saved = is_saved
        self.original_content = ""


class CustomTextEdit(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)

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


class Parser:
    def __init__(self):
        self.key_words = ["def", "class", "return", "if", "else", "while", "for", "and", "or"]

    def setup_colors(self):
        current_index = self.tab.current_index()
        tab_info = self.tab.tab_info[current_index]

        if self.key_words in tab_info.original_content:
            print("systemd in Linux!")

class Tab:
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.tab_info = []
        self.setup()

    def setup(self):
        self.tab_widget = QTabWidget()
        self.tab_widget.setMovable(True)
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed)

    def new_tab(self):
        tab_inside = QWidget()
        tab_lay = QVBoxLayout(tab_inside)
        tab_lay.setContentsMargins(0, 0, 0, 0)

        te = CustomTextEdit()
        te.textChanged.connect(lambda: self.text_changed())
        tab_lay.addWidget(te)

        tab_index = self.tab_widget.addTab(tab_inside, "Untitled")
        self.tab_widget.setCurrentIndex(tab_index)

        tab_info = TabInfo(tab_inside, te)
        tab_info.original_content = ""
        self.tab_info.insert(tab_index, tab_info)

        self.update_tab_title(tab_index)
        print("уставновка арч линукс бесплатна")

    def close_tab(self, index):
        if index >= len(self.tab_info):
            return

        self.tab_widget.currentChanged.disconnect(self.tab_changed)

        # удаление закрытой вкладки из списка с информацией о вкладке, навсегда, безвозвратно - не как .remove()
        del self.tab_info[index]
        self.tab_widget.removeTab(index)

        self.tab_widget.currentChanged.connect(self.tab_changed)

        if self.tab_widget.count() > 0:
            current_index = self.tab_widget.currentIndex()
            self.update_tab_title(current_index)

    def close_current_tab(self):
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            self.close_tab(current_index)

    def tab_changed(self, index):
        # с проверкой для того чтобы не произошёл IndexError
        if index >= 0 and index < len(self.tab_info):
            self.update_tab_title(index)

    def text_changed(self):
        current_index = self.tab_widget.currentIndex()
        if current_index >= 0:
            tab_info = self.tab_info[current_index]
            current_content = tab_info.text_edit.toPlainText()

            is_modified = current_content != tab_info.original_content
            tab_info.is_saved = not is_modified
            self.update_tab_title(current_index)

    def update_tab_title(self, index):
        # проверка для того чтобы не произошёл IndexError
        if index < 0 or index >= len(self.tab_info):
            return
        tab_info = self.tab_info[index]

        if tab_info.file_path:
            title = os.path.basename(tab_info.file_path)
        else:
            title = "Untitled"

        if not tab_info.is_saved:
            title += "*"

        self.tab_widget.setTabText(index, title)

    def save_tab_by_index(self, index, save_as_callback):
        tab_info = self.tab_info[index]

        if tab_info.file_path:
            # если существует
            return self.save_file(tab_info.file_path, index)
        else:
            # если новый
            return save_as_callback(index)

    def save_file(self, file_path, index):
        try:
            tab_info = self.tab_info[index]
            content = tab_info.text_edit.toPlainText()

            with open(file_path, "w", encoding="utf-8") as file:
                file.write(content)

            tab_info.file_path = file_path
            tab_info.original_content = content
            tab_info.is_saved = True

            self.update_tab_title(index)
            return True

        except Exception as e:
            print(f"Save error: {e}")
            return False

    def get_widget(self):
        return self.tab_widget

    def current_index(self):
        return self.tab_widget.currentIndex()

    def set_current_index(self, index):
        self.tab_widget.setCurrentIndex(index)
