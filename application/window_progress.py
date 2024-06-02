from PyQt6.QtWidgets import QVBoxLayout, QDialog, QProgressBar, QLabel
from PyQt6.QtCore import QSize, pyqtSignal, QThread

from utils import inference
from ultralytics import YOLO

from datetime import datetime


class InferenceThread(QThread):
    progress_signal = pyqtSignal(int)
    violations_signal = pyqtSignal(object)

    def __init__(self, video_path, model):
        super().__init__()
        self.running = True
        self.video_path = video_path
        self.model = model

    def run(self):
        while self.running:
            output = inference(self.video_path, self.model, callback=self.report_progress)
            print(datetime.now().strftime("%H:%M:%S"), ' - finish inference')

            violations = {}
            for key, value in output:
                if value == 1:
                    violations |= {round(key): str(value)}
            violations = merge_keys(violations, 8)

            self.violations_signal.emit(violations)
            self.running = False

    def report_progress(self, current, total):
        progress_percent = int((current / total) * 100)
        self.progress_signal.emit(progress_percent)

    def stop(self):
        self.running = False


class ProgressWindow(QDialog):
    signal = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.model = YOLO('../weights/YOLOv8_best.pt')

        self.setWindowTitle('Detecting')
        self.setFixedSize(300, 80)

        self.setModal(True)
        layout = QVBoxLayout()

        self.label = QLabel('Detecting violations...')
        layout.addWidget(self.label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setFixedSize(QSize(280, 20))
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

        self.thread = InferenceThread(self.parent.file_path, self.model)
        self.thread.progress_signal.connect(self.update_progress_bar)
        self.thread.violations_signal.connect(self.push)
        self.thread.start()

    def update_progress_bar(self, value):
        self.progress_bar.setValue(value)

    def push(self, signal_violations):
        self.signal.emit(signal_violations)
        self.accept()
        print(signal_violations)


def merge_keys(d, max_diff=5):
    keys = sorted(d.keys())
    result = {}
    prev_key = keys[0]

    for key in keys[1:]:
        if key - prev_key > max_diff:
            result[prev_key] = d[prev_key]
        prev_key = key

    # Add the last key if it's not added
    result[prev_key] = d[prev_key]

    return result