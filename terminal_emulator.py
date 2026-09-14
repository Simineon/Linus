from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLineEdit, QLabel, QTabWidget, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QProcess, QTimer
from PyQt6.QtGui import QFont, QTextCursor
import os
import platform
import re


class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.current_dir = os.getcwd()
        self.command_history = []
        self.history_index = -1
        self.setup()
        self.setWindowTitle("Terminal")
        self.resize(600, 400)

        self.waiting_for_cd_output = False

    def setup(self):
        self.lay = QVBoxLayout(self)
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.lay.setSpacing(0)

        self.tab_widget = QTabWidget()

        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: none;
                background-color: #1e1e1e;
            }
            QTabWidget::tab-bar {
                left: 5px;
            }
            QTabBar::tab {
                background: #2d2d2d;
                color: #cccccc;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background: #1e1e1e;
                border-bottom: 2px solid #007acc;
            }
            QTabBar::tab:hover {
                background: #3d3d3d;
            }
        """)
