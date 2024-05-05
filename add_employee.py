import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import conn

class AddEmployee(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Data")
        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.age_label = QLabel("Age:")
        self.age_input = QLineEdit()
        self.age_input.setReadOnly(False)
        layout.addWidget(self.age_label)
        layout.addWidget(self.age_input)

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
        name = self.nameInput.text()
        specialty_id = self.specialtyCombo.currentData()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO employees (id_specialty, surname, name) VALUES (%s, %s, %s)",
                        (specialty_id, name, ''))
            conn.commit()
            cur.close()
            conn.close()
            print("Сотрудник добавлен успешно.")
        except Exception as e:
            print(f"Ошибка при добавлении сотрудника: {e}")
            
    def loadSpecialties(self):
        try:
            cur = conn.cursor()
            cur.execute("SELECT id_specialty, name FROM specialties")
            specialties = cur.fetchall()
            for specialty in specialties:
                self.specialtyCombo.addItem(specialty[1], specialty[0])
            cur.close()
            conn.close()
            self.name_input.setReadOnly(False)
        except Exception as e:
            print(f"Ошибка при загрузке специальностей: {e}")
