import cv2
from PyQt6.QtWidgets import *

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer


class VideoWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()

        self.setWindowTitle("Camera")
        self.file = cv2.VideoCapture(path)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(640, 480)

        self.play_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "")
        self.play_button.clicked.connect(self.toggle_play)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, int(self.file.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.slider.sliderMoved.connect(self.set_position)
        self.slider.setEnabled(False)

        self.time_input = QLineEdit(self)
        self.time_input.setPlaceholderText("Enter time in seconds")

        self.jump_button = QPushButton("Jump")
        self.jump_button.clicked.connect(self.jump_to_time)

        time_layout = QHBoxLayout()
        time_layout.addWidget(self.time_input)
        time_layout.addWidget(self.jump_button)

        control_layout = QHBoxLayout()
        control_layout.addWidget(self.play_button)
        control_layout.addWidget(self.slider)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.image_label)
        layout.addLayout(control_layout)
        layout.addLayout(time_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

        self.is_paused = False
        self.first = True

    def update_frame(self):

        if not self.is_paused:
            ret, frame = self.file.read()

            if ret:
                frame = cv2.resize(frame, (640, 480))
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape

                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                pixmap = QPixmap.fromImage(qt_image)
                self.image_label.setPixmap(pixmap)

                current_frame = int(self.file.get(cv2.CAP_PROP_POS_FRAMES))
                self.slider.setValue(current_frame)

        if self.first:
            self.is_paused = True
            self.first = False

    def toggle_play(self):
        if self.is_paused:
            self.is_paused = False
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.timer.start(33)
            self.slider.setEnabled(False)
        else:
            self.is_paused = True
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.timer.stop()
            self.slider.setEnabled(True)

    def set_position(self, position):
        self.file.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.update_frame()
        if not self.is_paused:
            self.toggle_play()

    def jump_to_time(self, timestamp=None):
        if timestamp:
            time_in_seconds = float(timestamp)
        else:
            time_in_seconds = float(self.time_input.text())

        print(f"Current timestamp: {time_in_seconds}")

        fps = self.file.get(cv2.CAP_PROP_FPS)
        frame_number = int(time_in_seconds * fps)
        self.file.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.first = True
        self.is_paused = False
        self.update_frame()







