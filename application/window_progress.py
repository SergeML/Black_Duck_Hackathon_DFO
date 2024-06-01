from PyQt6.QtWidgets import QVBoxLayout, QDialog, QProgressBar, QLabel
from PyQt6.QtCore import QTimer, QSize, pyqtSignal


class ProgressWindow(QDialog):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.progress_value = 0
        self.timer.start(20)

    def update_progress(self):
        self.progress_value += 1
        self.progress_bar.setValue(self.progress_value)
        if self.progress_value >= 100:
            self.timer.stop()
            self.accept()
            self.signal.emit('trigger')
