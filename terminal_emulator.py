from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TerminalWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        self.lay = QVBoxLayout(self)

        term_label = QLabel("Terminal Emulator")
        self.lay.addWidget(term_label)

