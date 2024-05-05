import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import conn

class AddNorm(QDialog):
    def __init__(self):
        super().__init__()

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
        
        self.specialtyLabel = QLabel('Разряд:')
        self.specialtyCombo = QComboBox()
        self.loadSpecialties()
        layout.addWidget(self.specialtyLabel)
        layout.addWidget(self.specialtyCombo)

        self.setLayout(layout)
        
        

    def submit_data(self):
        name = self.name_input.text()
        surname = self.surname_input.text()
        rank_id = self.specialtyCombo.currentData()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO norms (id_rank, name, description) VALUES (%s, %s, %s)",
                        (rank_id, name, surname))
            conn.commit()
            cur.close()
            print("Сотрудник добавлен успешно.")
            self.close()
        except Exception as e:
            print(f"Ошибка при добавлении нормы: {e}")
            
    def loadSpecialties(self):
        try:
            cur = conn.cursor()
            cur.execute("SELECT id_rank, name FROM ranks")
            specialties = cur.fetchall()
            for specialty in specialties:
                self.specialtyCombo.addItem(specialty[1], specialty[0])
            cur.close()
        except Exception as e:
            print(f"Ошибка при загрузке разрядов: {e}")
