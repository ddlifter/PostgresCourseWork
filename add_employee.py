import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

from PyQt5.QtCore import Qt

class AddEmployee(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn : ConnectionManager = conn
        self.setFixedSize(250, 230)

        self.setWindowTitle("Добавить данные")
        layout = QVBoxLayout()

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        self.surname_input.setReadOnly(False)
        self.surname_input.textChanged.connect(self.check_inputs)  # Проверка фамилии при изменении текста
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        self.name_input.textChanged.connect(self.check_inputs)  # Проверка имени при изменении текста
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.setLayout(layout)
        
        self.specialtyLabel = QLabel('Специальность:')
        self.specialtyCombo = QComboBox()
        self.loadSpecialties()
        layout.addWidget(self.specialtyLabel)
        layout.addWidget(self.specialtyCombo)
        
        self.submit_button = QPushButton("Подтвердить")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        # Добавим кнопку "Submit" и сделаем ее неактивной изначально
        self.submit_button.setEnabled(False)

    def check_inputs(self):
        surname = self.surname_input.text()
        name = self.name_input.text()

        # Проверяем, что оба поля не пустые и не содержат цифры
        if surname and name and surname.isalpha() and name.isalpha():
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit_data(self):
        # Оставляем ваш существующий код без изменений
        with self.conn as conn:
            with conn.cursor() as cur:
                name = self.name_input.text()
                surname = self.surname_input.text()
                specialty_id = self.specialtyCombo.currentData()
                try:
                    cur.execute("INSERT INTO employees (id_specialty, surname, name) VALUES (%s, %s, %s)",
                                (specialty_id, surname, name))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Информация о сотруднике успешно добавлена.")
                    self.accept()
                except Exception as e:
                    print(f"Ошибка при добавлении сотрудника: {e}")
            
    def loadSpecialties(self):
        # Оставляем ваш существующий код без изменений
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_specialty, name FROM specialties")
                    specialties = cur.fetchall()
                    for specialty in specialties:
                        self.specialtyCombo.addItem(specialty[1], specialty[0])
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке специальностей: {e}")

