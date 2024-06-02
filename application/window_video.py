import cv2
from PyQt6.QtWidgets import *

from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import Qt, QTimer


class VideoWindow(QMainWindow):
    def __init__(self, path):
        super().__init__()

        self.file = cv2.VideoCapture(path)

        original_fps = self.file.get(cv2.CAP_PROP_FPS)
        frame_count = int(self.file.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / original_fps

        self.mins, self.secs = divmod(duration, 60)
        self.time = 1000/round(original_fps)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(640, 480)

        self.play_button = QPushButton(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "")
        self.play_button.clicked.connect(self.toggle_play)

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, int(self.file.get(cv2.CAP_PROP_FRAME_COUNT)))
        self.slider.sliderReleased.connect(self.set_position)
        self.slider.setEnabled(True)

        self.slider.setStyleSheet("""
                    QSlider::handle:horizontal {
                        background-color: #5c5c5c;
                        border: 1px solid #5c5c5c;
                        width: 8px;
                        height: 8px;
                        border-radius: 2px;
                        margin: -6px 0; 
                    }
                    QSlider::groove:horizontal {
                        background: #bcbcbc;
                        height: 4px;
                    }
                    QSlider::sub-page:horizontal {
                        background: #5c5c5c;
                    }
                """)

        self.timer_label = QLabel(self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setFixedSize(100, 30)
        self.update_timer(0)

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
        control_layout.addWidget(self.timer_label)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.image_label)
        layout.addLayout(control_layout)
        layout.addLayout(time_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(self.time)

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
                self.update_timer(current_frame / self.file.get(cv2.CAP_PROP_FPS))

        if self.first:
            self.is_paused = True
            self.first = False

    def toggle_play(self):
        if self.is_paused:
            self.is_paused = False
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))
            self.timer.start(self.time)
            self.slider.setEnabled(False)
        else:
            self.is_paused = True
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
            self.timer.stop()
            self.slider.setEnabled(True)

    def set_position(self):
        position = self.slider.value()
        self.file.set(cv2.CAP_PROP_POS_FRAMES, position)
        self.first = True
        self.is_paused = False

        self.update_frame()

    def jump_to_time(self, timestamp=None):
        if timestamp:
            time_in_seconds = float(timestamp)
        else:
            try:
                time_in_seconds = float(self.time_input.text())
            except ValueError:
                return

        print(f"Current timestamp: {time_in_seconds}")

        fps = self.file.get(cv2.CAP_PROP_FPS)
        frame_number = int(time_in_seconds * fps)
        self.file.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        self.first = True
        self.is_paused = False
        self.update_frame()

    def update_timer(self, seconds):
        mins, secs = divmod(seconds, 60)
        time_str = f'{int(mins):02}:{int(secs):02}/{int(self.mins):02}:{int(self.secs):02}'
        self.timer_label.setText(time_str)