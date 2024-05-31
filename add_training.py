import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox, QDateEdit
import psycopg2
from PyQt5.QtCore import QDate
from connection import ConnectionManager

class AddTraining(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn : ConnectionManager = conn
        self.setFixedSize(250, 230)

        self.setWindowTitle("Добавить данные")
        layout = QVBoxLayout()

        self.date_label = QLabel("Дата:")
        layout.addWidget(self.date_label)

        # Поле для ввода даты с раскрывающимся календарем
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Включаем возможность открытия календаря
        self.date_input.setDate(QDate.currentDate())  # Устанавливаем текущую дату как начальную
        layout.addWidget(self.date_input)

        # Устанавливаем макет в виджет
        self.setLayout(layout)
        self.setWindowTitle("Добавить данные")

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
        
        self.submit_button = QPushButton("Подтвердить")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)
        


    def submit_data(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                name = self.date_input.text()
                empl_id = self.specialtyCombo.currentData()
                norm_id = self.specialtyCombo2.currentData()
                try:
                    cur.execute("INSERT INTO training(id_employee, id_norm, data) VALUES (%s, %s, %s)",
                                (empl_id, norm_id, name))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Информация об обучении успешно добавлена.")
                    self.accept()
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
