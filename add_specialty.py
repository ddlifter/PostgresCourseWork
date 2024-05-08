import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

class AddRank(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn = conn
        self.conn = self.conn.connect()

        self.setWindowTitle("Add Data")
        layout = QVBoxLayout()
        
        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.surname_label = QLabel("Description:")
        self.surname_input = QLineEdit()
        self.surname_input.setReadOnly(False)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_data(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO ranks (name, description) VALUES (%s, %s)",
                        (name, surname))
            self.conn.commit()
            cur.close()
            print("Разряд добавлен успешно.")
            self.close()
        except Exception as e:
            print(f"Ошибка при добавлении разряда: {e}")
            