from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, pyqtSignal


class TableWindow(QDialog):
    signal = pyqtSignal(str)

    def __init__(self, violation):
        super().__init__()

        self.violation = violation

        self.setWindowTitle("violation")
        self.setMinimumSize(QSize(500, 200))

        self.table = QTableWidget(self)
        self.init_table()

        self.button_export = QPushButton('Export', self)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button_export)

    def init_table(self):
        self.table.setColumnCount(4)
        self.table.setRowCount(len(self.violation))
        self.table.setHorizontalHeaderLabels(["id", "timestamp", "violation type", "jump"])

        for row, (key, value) in enumerate(self.violation.items()):
            id = QTableWidgetItem(str(row))
            timestamp = QTableWidgetItem(str(key))
            violation_type = QTableWidgetItem(value)

            self.table.setItem(row, 0, id)
            self.table.setItem(row, 1, timestamp)
            self.table.setItem(row, 2, violation_type)

            button_jump = QPushButton("jump", self)
            button_jump.clicked.connect(lambda _, x=self.table.item(row, 1).text(): self.send(x))

            self.table.setCellWidget(row, 3, button_jump)

    def send(self, key):
        self.signal.emit(key)





