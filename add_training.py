import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

class AddTraining(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn : ConnectionManager = conn

        self.setWindowTitle("Add Data")
        layout = QVBoxLayout()

        self.name_label = QLabel("Name:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)
        
        self.specialtyLabel = QLabel('Сотрудник:')
        self.specialtyCombo = QComboBox()
        self.loadEmployees()
        layout.addWidget(self.specialtyLabel)
        layout.addWidget(self.specialtyCombo)
        
        self.specialtyLabel2 = QLabel('Норма:')
        self.specialtyCombo2 = QComboBox()
        self.loadNorms()
        layout.addWidget(self.specialtyLabel2)
        layout.addWidget(self.specialtyCombo2)

    def submit_data(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                name = self.name_input.text()
                empl_id = self.specialtyCombo.currentData()
                norm_id = self.specialtyCombo2.currentData()
                try:
                    cur.execute("INSERT INTO training(id_employee, id_norm, data) VALUES (%s, %s, %s)",
                                (empl_id, norm_id, name))
                    conn.commit()
                    cur.close()
                    print("Сотрудник добавлен успешно.")
                    self.close()
                except Exception as e:
                    print(f"Ошибка при добавлении сотрудника: {e}")
            
    def loadEmployees(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_employee, surname FROM employees")
                    specialties = cur.fetchall()
                    for specialty in specialties:
                        self.specialtyCombo.addItem(specialty[1], specialty[0])
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке специальностей: {e}")
                    
    def loadNorms(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_norm, name FROM norms")
                    specialties = cur.fetchall()
                    for specialty in specialties:
                        self.specialtyCombo2.addItem(specialty[1], specialty[0])
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке специальностей: {e}")
