from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QDialog, QComboBox, QDateEdit, QMessageBox
from PyQt5.QtCore import QDate
from connection import ConnectionManager

class UpdateTraining(QDialog):
    def __init__(self, conn: ConnectionManager, training_id: int):
        super().__init__()
        self.conn: ConnectionManager = conn
        self.training_id = training_id

        self.setWindowTitle("Update Data")
        layout = QVBoxLayout()

        self.date_label = QLabel("Дата:")
        layout.addWidget(self.date_label)

        # Поле для ввода даты с раскрывающимся календарем
        self.date_input = QDateEdit()
        self.date_input.setCalendarPopup(True)  # Включаем возможность открытия календаря
        layout.addWidget(self.date_input)

        # Устанавливаем макет в виджет
        self.setLayout(layout)
        self.setWindowTitle("Выбор даты")

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

        self.load_training_data()

    def load_training_data(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_employee, id_norm, data FROM training WHERE id_training = %s", (self.training_id,))
                    training_data = cur.fetchone()
                    if training_data:
                        employee_id, norm_id, date = training_data
                        self.specialtyCombo.setCurrentIndex(self.specialtyCombo.findData(employee_id))
                        self.specialtyCombo2.setCurrentIndex(self.specialtyCombo2.findData(norm_id))
                        self.date_input.setDate(QDate.fromString(date.strftime("%Y-%m-%d"), "yyyy-MM-dd"))
                    cur.close()
                except Exception as e:
                    print(f"Ошибка при загрузке данных тренировки: {e}")

    def submit_data(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                name = self.date_input.date().toString("yyyy-MM-dd")
                empl_id = self.specialtyCombo.currentData()
                norm_id = self.specialtyCombo2.currentData()
                try:
                    cur.execute("UPDATE training SET id_employee = %s, id_norm = %s, data = %s WHERE id_training = %s",
                                (empl_id, norm_id, name, self.training_id))
                    conn.commit()
                    cur.close()
                    QMessageBox.information(self, "Успех", "Данные обновлены успешно.")
                    self.close()
                    
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
