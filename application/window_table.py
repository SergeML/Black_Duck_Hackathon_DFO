from PyQt6.QtWidgets import *
from PyQt6.QtCore import QSize, pyqtSignal
import pandas as pd
import datetime


class TableWindow(QDialog):
    signal = pyqtSignal(str)

    def __init__(self, violation, parent=None):
        super().__init__()
        self.parent = parent
        self.violation = violation

        self.setWindowTitle("violation")
        self.setMinimumSize(QSize(525, 400))

        self.table = QTableWidget(self)
        self.init_table()

        self.button_export = QPushButton('Export', self)
        self.button_export.clicked.connect(self.export)

        self.layout = QVBoxLayout(self)

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.button_export)

    def init_table(self):
        self.table.setColumnCount(5)
        self.table.setRowCount(len(self.violation))
        self.table.setHorizontalHeaderLabels(["id", "timestamp", "violation type", "jump", ""])

        width_columns = [50, 125, 200, 50, 50]
        for idx, value in enumerate(width_columns):
            self.table.setColumnWidth(idx, value)

        for row, (key, value) in enumerate(self.violation.items()):
            id = QTableWidgetItem(str(row))
            mins, secs = divmod(key, 60)

            timestamp = QTableWidgetItem(f'{mins:02}:{secs:02}')
            violation_type = QTableWidgetItem(value)

            self.table.setItem(row, 0, id)
            self.table.setItem(row, 1, timestamp)
            self.table.setItem(row, 2, violation_type)

            button_jump = QPushButton("jump", self)
            button_jump.clicked.connect(lambda _, x=self.table.item(row, 1).text(): self.send(x))

            checkbox = QCheckBox()

            lay = QHBoxLayout()
            lay.addSpacing(10)
            lay.addWidget(checkbox)

            widget = QWidget()
            widget.setLayout(lay)

            self.table.setCellWidget(row, 3, button_jump)
            self.table.setCellWidget(row, 4, widget)

    def send(self, key):
        mins, secs = [int(x) for x in key.split(":")]
        key = str(mins*60 + secs)
        self.signal.emit(key)

    def export(self):
        filename = f'../reports/{self.parent.file_path.split("/")[-1][:-4]}_violations'
        file_path, _ = QFileDialog.getSaveFileName(None,  "Save CSV", filename, "CSV Files (*.csv);;All Files (*)")

        if file_path:
            data = []

            for row in range(self.table.rowCount()):
                widget = self.table.cellWidget(row, 4)
                checkbox = widget.layout().itemAt(1).widget()

                if checkbox.isChecked():
                    id = self.table.item(row, 0).text()
                    timestamp = self.table.item(row, 1).text()
                    violation_type = self.table.item(row, 2).text()

                    data.append([id, timestamp, violation_type])

            df = pd.DataFrame(data, columns=["id", "timestamp", "violation type"])
            df.to_csv(file_path, index=False)

            QMessageBox.information(self, 'Message', 'File has been save')


















