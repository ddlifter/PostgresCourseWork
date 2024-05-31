import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QDialog, QMessageBox, QComboBox
import psycopg2
from connection import ConnectionManager

class AddNorm(QDialog):
    def __init__(self, conn: ConnectionManager):
        super().__init__()
        self.conn : ConnectionManager = conn
        self.setFixedSize(250, 230)

        self.setWindowTitle("Добавить данные")
        layout = QVBoxLayout()
        
        self.name_label = QLabel("Название:")
        self.name_input = QLineEdit()
        self.name_input.setReadOnly(False)
        self.name_input.textChanged.connect(self.check_inputs)
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)

        self.surname_label = QLabel("Описание:")
        self.surname_input = QLineEdit()
        self.surname_input.setReadOnly(False)
        self.surname_input.textChanged.connect(self.check_inputs)
        layout.addWidget(self.surname_label)
        layout.addWidget(self.surname_input)
        
        self.specialtyLabel = QLabel('Разряд:')
        self.specialtyCombo = QComboBox()
        self.loadSpecialties()
        layout.addWidget(self.specialtyLabel)
        layout.addWidget(self.specialtyCombo)

        self.setLayout(layout)
        
        self.submit_button = QPushButton("Подтвердить")
        self.submit_button.clicked.connect(self.submit_data)
        layout.addWidget(self.submit_button)
        
        self.submit_button.setEnabled(False)
        
    def check_inputs(self):
        surname = self.surname_input.text().strip()
        name = self.name_input.text().strip()

        if surname and name and surname.isalpha() and name.isalpha():
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def submit_data(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                name = self.name_input.text()
                surname = self.surname_input.text()
                rank_id = self.specialtyCombo.currentData()
                try:
                    cur.execute("INSERT INTO norms (id_rank, name, description) VALUES (%s, %s, %s)",
                                (rank_id, name, surname))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Информация о норме успешно добавлена.")
                    self.accept()
                except Exception as e:
                    print(f"Ошибка при добавлении нормы: {e}")
            
    def loadSpecialties(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_rank, name FROM ranks")
                    specialties = cur.fetchall()
                    if not specialties:
                        QMessageBox.warning(self, "Отсутствуют разряды", "Нет доступных разрядов. Пожалуйста, добавьте разряды.")
                        self.reject()
                    else:
                        for specialty in specialties:
                            self.specialtyCombo.addItem(specialty[1], specialty[0])
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке разрядов: {e}")

