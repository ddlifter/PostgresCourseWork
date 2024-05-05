from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget


class Specialties(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.showMaximized()
        self.label = QLabel("This is Form 2")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)