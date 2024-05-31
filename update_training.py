from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QDialog, QComboBox, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
from connection import ConnectionManager

class UpdateTraining(QDialog):
    def __init__(self, conn: ConnectionManager, training_id: int):
        super().__init__()
        self.conn: ConnectionManager = conn
        self.setFixedSize(250, 230)
        self.training_id = training_id

        self.setWindowTitle("Изменить данные")
        layout = QVBoxLayout()

        self.date_label = QLabel("Дата:")
        layout.addWidget(self.date_label)

        # Поле для ввода даты с раскрывающимся календарем
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Включаем возможность открытия календаря
        layout.addWidget(self.date_input)

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
        name = self.date_input.date().toString("yyyy-MM-dd")
        empl_id = self.specialtyCombo.currentData()
        norm_id = self.specialtyCombo2.currentData()
        
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("UPDATE training SET id_employee = %s, id_norm = %s, data = %s WHERE id_training = %s",
                                (empl_id, norm_id, name, self.training_id))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Данные обновлены успешно.")
                    self.accept()
                    
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Ошибка при обновлении данных тренировки: {e}")

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
                    print(f"Ошибка при загрузке сотрудников: {e}")

    def loadNorms(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_norm, name FROM norms")
                    norms = cur.fetchall()
                    for norm in norms:
                        self.specialtyCombo2.addItem(norm[1], norm[0])
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке норм: {e}")
