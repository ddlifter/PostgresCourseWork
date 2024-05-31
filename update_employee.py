import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

class UpdateEmployee(QDialog):
    def __init__(self, conn: ConnectionManager, id_employee, surname, name):
        super().__init__()
        self.conn: ConnectionManager = conn
        self.id_employee = id_employee
        self.setFixedSize(250, 230)

        self.setWindowTitle("Изменить данные")
        layout = QVBoxLayout()

        self.surname_label = QLabel("Фамилия:")
        self.surname_input = QLineEdit()
        self.surname_input.setText(surname)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)

        self.name_label = QLabel("Имя:")
        self.name_input = QLineEdit()
        self.name_input.setText(name)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.specialty_label = QLabel("Специальность:")
        self.specialty_combo = QComboBox()
        layout.addWidget(self.specialty_label)
        layout.addWidget(self.specialty_combo)

        self.submit_button = QPushButton("Подтвердить")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

        self.load_specialties()

    def load_specialties(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_specialty, name FROM specialties")
                    specialties = cur.fetchall()
                    for specialty_id, specialty_name in specialties:
                        self.specialty_combo.addItem(specialty_name, specialty_id)
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить специальности: {str(e)}")

    def submit_data(self):
        new_surname = self.surname_input.text()
        new_name = self.name_input.text()
        new_specialty_id = self.specialty_combo.currentData()

        if not new_surname or not new_name:
            QMessageBox.critical(self, "Ошибка", "Фамилия и имя не могут быть пустыми.")
            return

        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("UPDATE employees SET surname = %s, name = %s, id_specialty = %s WHERE id_employee = %s",
                                (new_surname, new_name, new_specialty_id, self.id_employee))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Информация о сотруднике успешно обновлена.")
                    self.accept()  # Закрыть диалоговое окно
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось обновить информацию о сотруднике: {str(e)}")
