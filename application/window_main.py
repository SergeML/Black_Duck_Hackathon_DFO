from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize

from window_video import VideoWindow
from window_table import TableWindow
from window_progress import ProgressWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.violation = None
        self.video_window = None

        self.setWindowTitle("Automation of detection technological violations")
        size = QSize(200, 60)

        self.stub_image = QLabel(self)
        self.stub_image.setFixedSize(640, 480)
        self.stub_image.setStyleSheet("background-color: #BDBDBD;")

        self.button_1 = QPushButton("Choice Video File")
        self.button_1.clicked.connect(self.choice_video_file)
        self.button_1.setFixedSize(size)

        self.button_2 = QPushButton("Detection")
        self.button_2.clicked.connect(self.detection)
        self.button_2.setFixedSize(size)
        self.button_2.setEnabled(False)

        self.button_3 = QPushButton("Report")
        self.button_3.clicked.connect(self.show_result)
        self.button_3.setFixedSize(size)
        self.button_3.setEnabled(False)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.button_1)
        buttons_layout.addWidget(self.button_2)
        buttons_layout.addWidget(self.button_3)

        vertical_line = QFrame()
        vertical_line.setFrameShape(QFrame.Shape.VLine)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.stub_image)
        self.main_layout.addWidget(vertical_line)
        self.main_layout.addLayout(buttons_layout)
        self.main_layout.addWidget(vertical_line)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def choice_video_file(self):
        file_dialog = QFileDialog(self)
        self.file_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi)")

        if self.file_path:
            self.button_3.setEnabled(False)
            self.main_layout.replaceWidget(self.video_window, self.stub_image)
            if self.video_window:
                self.video_window.deleteLater()

            self.video_window = VideoWindow(self.file_path)
            self.video_window.show()

            self.main_layout.replaceWidget(self.stub_image, self.video_window)
            self.stub_image.hide()
            self.button_2.setEnabled(True)

    def detection(self):
        window = ProgressWindow(self)
        window.signal.connect(self.get_violation)
        window.exec()

    def get_violation(self, violation=None):
        self.violation = violation
        if self.violation is not None:
            self.button_3.setEnabled(True)
            QMessageBox.information(self, 'Message', 'Violations were found. Details in the report')
        else:
            QMessageBox.information(self, 'Message', 'No violations were found')

    def show_result(self):
        window = TableWindow(self.violation, self)
        window.signal.connect(self.jump)
        window.show()

    def jump(self, key):
        timestamp = key
        self.video_window.jump_to_time(timestamp)