from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize

from window_video import VideoWindow
from window_table import TableWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Automation of detection technological violations")
        self.setGeometry(100, 100, 800, 600)
        size = QSize(200, 60)

        self.stub_image = QLabel(self)
        self.stub_image.setFixedSize(640, 480)
        self.stub_image.setStyleSheet("background-color: gray;")

        self.camera_window = None

        self.button_1 = QPushButton("Choose Video File")
        self.button_1.clicked.connect(self.choose_video_file)
        self.button_1.setFixedSize(size)

        self.button_2 = QPushButton("Detection")
        self.button_2.clicked.connect(self.detection)
        self.button_2.setFixedSize(size)
        self.button_2.setEnabled(False)

        self.button_3 = QPushButton("Show Result")
        self.button_3.clicked.connect(self.show_result)
        self.button_3.setFixedSize(size)
        self.button_3.setEnabled(False)

        self.button_4 = QPushButton("some button")
        self.button_4.setFixedSize(size)

        buttons_layout = QVBoxLayout()
        buttons_layout.addWidget(self.button_1)
        buttons_layout.addWidget(self.button_2)
        buttons_layout.addWidget(self.button_3)
        buttons_layout.addWidget(self.button_4)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.stub_image)
        self.main_layout.addLayout(buttons_layout)

        central_widget = QWidget()
        central_widget.setLayout(self.main_layout)
        self.setCentralWidget(central_widget)

    def choose_video_file(self):
        file_dialog = QFileDialog(self)
        self.file_path, _ = file_dialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi)")

        if self.file_path:
            self.main_layout.replaceWidget(self.camera_window, self.stub_image)
            if self.camera_window:
                self.camera_window.deleteLater()

            self.camera_window = VideoWindow(self.file_path)
            self.camera_window.show()

            self.main_layout.replaceWidget(self.stub_image, self.camera_window)
            self.stub_image.hide()
            self.button_2.setEnabled(True)

    def detection(self):
        #violation = model.inference(self.file_path)

        print('Done')

        self.violation = {
            10: 'violation type 0',
            54: 'violation type 1',
            175: 'violation type 2',
            200: 'violation type 1',
        }

        self.button_3.setEnabled(True)

    def show_result(self):
        window = TableWindow(self.violation)
        window.signal.connect(self.jump)
        window.show()

    def jump(self, key):
        timestamp = key
        self.camera_window.jump_to_time(timestamp)















