from PyQt6.QtCore import Qt, QDir, QModelIndex
from PyQt6.QtGui import QAction, QFileSystemModel
from PyQt6.QtWidgets import QMenu, QWidget, QMenuBar, QHBoxLayout, QVBoxLayout, QSplitter, QFrame, \
    QLabel, QFileDialog, QTreeView, QPushButton
from tab import Tab
from runner import Runner
from terminal_emulator import TerminalWidget


class AppWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setup()
        self.setWindowTitle("Rust лучший яп")

    def setup(self):
        self.lay = QVBoxLayout(self)
        self.menuBar = QMenuBar()

        self.splitter = QSplitter(Qt.Orientation.Horizontal)

        self.tab = Tab(self)
        self.setupExplorer()

        self.splitter.addWidget(self.tab.get_widget())
        self.splitter.setSizes([300, 500])

        self.lay.addWidget(self.splitter)

        self.setupMenu()
        self.tab.new_tab()

        self.setupStyle()

    def setupStyle(self):
        try:
            with open("static/style.qss", encoding="utf-8") as st_file:
                self.setStyleSheet(st_file.read())
        except FileNotFoundError:
            print("Style file not found, using default static")

    def setupMenu(self):
        self.fileMenu = self.menuBar.addMenu("&File")
        self.runMenu = self.menuBar.addMenu("&Run")
        self.terminalMenu = self.menuBar.addMenu("&Terminal")

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

        self.save_file_action = QAction("Save File", self)
        self.save_file_action.setShortcut("Ctrl+S")
        self.save_file_action.triggered.connect(self.saveNewFile)

        self.save_as_action = QAction("Save As...", self)
        self.save_as_action.setShortcut("Ctrl+Shift+S")
        self.save_as_action.triggered.connect(self.save_as_current)

        self.choose_run_file = QAction("Choose file which will run", self)
        self.choose_run_file.setShortcut("Ctrl+Shift+R")
        self.choose_run_file.triggered.connect(self.choose_run)

        self.run_current_file = QAction("Run current file in tab", self)
        self.run_current_file.setShortcut("Ctrl+R")
        self.run_current_file.triggered.connect(self.run_current)

        self.open_terminal = QAction("Open terminal")
        self.open_terminal.setShortcut("F4")
        self.open_terminal.triggered.connect(self.open_terminal_window)

        self.fileMenu.addAction(self.save_as_action)
        self.fileMenu.addAction(self.newFile)
        self.fileMenu.addAction(self.open_action)
        self.fileMenu.addAction(self.open_folder_action)
        self.fileMenu.addAction(self.save_file_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.close_tab_action)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction("Exit", self.close)

        self.runMenu.addAction(self.choose_run_file)
        self.runMenu.addAction(self.run_current_file)

        self.terminalMenu.addAction(self.open_terminal)

        self.lay.setMenuBar(self.menuBar)

    def setupExplorer(self):
        self.explorer_frame = QFrame()
        self.explorer_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.explorer_frame.setMinimumWidth(200)

        explorer_layout = QVBoxLayout(self.explorer_frame)
        explorer_layout.setContentsMargins(0, 0, 0, 0)

        header_layout = QHBoxLayout()
        self.explorerLabel = QLabel("Directory's tree")
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

            self.file_tree.expand(index)

            print(f"Opened folder: {folder_path}")

    def openFile(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory=QDir.homePath()
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()

                    self.new_tab()
                    current_index = self.tab.current_index()
                    tab_info = self.tab.tab_info[current_index]

                    tab_info.text_edit.setPlainText(content)
                    tab_info.file_path = file_path
                    tab_info.original_content = content
                    tab_info.is_saved = True

                    self.tab.update_tab_title(current_index)
                    print(f"Opened file: {file_path}")

            except Exception as e:
                print(f"Error reading file: {e}")

    def on_file_double_click(self, index: QModelIndex):
        file_path = self.file_model.filePath(index)

        for i in range(len(self.tab.tab_info)):
            tab_info = self.tab.tab_info[i]
            if tab_info.file_path == file_path:
                self.tab.set_current_index(i)
                return

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

                self.new_tab()
                current_index = self.tab.current_index()
                tab_info = self.tab.tab_info[current_index]

                tab_info.text_edit.setPlainText(content)
                tab_info.file_path = file_path
                tab_info.original_content = content
                tab_info.is_saved = True

                self.tab.update_tab_title(current_index)
                print(f"Opened file from explorer: {file_path}")

        except Exception as e:
            print("Error: ", e)

    def new_tab(self):
        self.tab.new_tab()

    def close_current_tab(self):
        self.tab.close_current_tab()

    def saveNewFile(self):
        current_index = self.tab.current_index()
        if current_index < 0:
            return

        self.tab.save_tab_by_index(current_index, self.save_as_file_dialog)

    def save_as_file_dialog(self, index):
        file_path, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption='Save file',
            directory=QDir.homePath()
        )

        if file_path:
            return self.tab.save_file(file_path, index)
        return False

    def save_as_current(self):
        current_index = self.tab.current_index()
        if current_index >= 0:
            self.save_as_file_dialog(current_index)

    def choose_run(self):
        file_path, _ = QFileDialog.getOpenFileName(
            parent=self,
            caption='Open file',
            directory=QDir.homePath()
        )

        try:
            current_index = self.tab.current_index()
            tab_info = self.tab.tab_info[current_index]
            tab_info.file_path = file_path

            self.runner = Runner(file_path)
            self.runner.runPython()
        except Exception as e:
            print(e)

    def run_current(self):
        try:
            current_index = self.tab.current_index()
            tab_info = self.tab.tab_info[current_index]
            file_pyth = tab_info.file_path

            self.runner = Runner(file_pyth)
            self.runner.runPython()
        except Exception as e:
            print(e)

    def open_terminal_window(self):
        terminal_window_widget = TerminalWidget()
        terminal_window_widget.resize(400, 400)
        terminal_window_widget.show()

        current_index = terminal_window_widget.tab.current_index()
        tab_info = terminal_window_widget.tab.tab_info[current_index]

        tab_info.text_edit.setPlainText(self.runner.get_output())

    # на будущее
    def closeEvent(self, event):
        pass
