import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

class AddEmployee(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn = conn
        self.conn = self.conn.connect()

        self.setWindowTitle("Add Data")
        layout = QVBoxLayout()

        self.surname_label = QLabel("SurName:")
        self.surname_input = QLineEdit()
        self.surname_input.setReadOnly(False)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        
        self.specialtyLabel = QLabel('Специальность:')
        self.specialtyCombo = QComboBox()
        self.loadSpecialties()
        layout.addWidget(self.specialtyLabel)
        layout.addWidget(self.specialtyCombo)

    def submit_data(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        specialty_id = self.specialtyCombo.currentData()
        try:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO employees (id_specialty, surname, name) VALUES (%s, %s, %s)",
                        (specialty_id, surname, name))
            self.conn.commit()
            cur.close()
            print("Сотрудник добавлен успешно.")
            self.close()
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")
            
    def loadSpecialties(self):
        try:
            cur = self.conn.cursor()
            cur.execute("SELECT id_specialty, name FROM specialties")
            specialties = cur.fetchall()
            for specialty in specialties:
                self.specialtyCombo.addItem(specialty[1], specialty[0])
            cur.close()
        except Exception as e:
            print(f"Ошибка при загрузке специальностей: {e}")
