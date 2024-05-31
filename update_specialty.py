from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from connection import ConnectionManager

class UpdateSpecialty(QDialog):
    def __init__(self, conn: ConnectionManager, spec_id, spec_name, description):
        super().__init__()
        self.conn = conn
        self.setFixedSize(250, 230)
        self.spec_id = spec_id
        self.spec_name = spec_name
        self.description = description
        self.setWindowTitle("Изменить данные")
        
        layout = QVBoxLayout()
        
        self.spec_name_label = QLabel("Название специальности:")
        self.spec_name_edit = QLineEdit()
        self.spec_name_edit.setText(self.spec_name)
        layout.addWidget(self.spec_name_label)
        layout.addWidget(self.spec_name_edit)
        
        self.description_label = QLabel("Описание:")
        self.description_edit = QLineEdit()
        self.description_edit.setText(self.description)
        layout.addWidget(self.description_label)
        layout.addWidget(self.description_edit)
        
        self.update_button = QPushButton("Подтвердить")
        self.update_button.clicked.connect(self.update_specialty)
        layout.addWidget(self.update_button)
        
        self.setLayout(layout)
        
    def update_specialty(self):
        new_spec_name = self.spec_name_edit.text()
        new_description = self.description_edit.text()
        
        if not new_spec_name or not new_description:
            QMessageBox.critical(self, "Ошибка", "Поля не могут быть пустыми.")
            return
        
        if any(char.isdigit() for char in new_spec_name) or any(char.isdigit() for char in new_description):
            QMessageBox.critical(self, "Ошибка", "Поля не могут содержать цифры.")
            return
        
        with self.conn as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("UPDATE specialties SET name = %s, description = %s WHERE id_specialty = %s", (new_spec_name, new_description, self.spec_id))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Данные успешно обновлены.")
                    self.accept()  # Закрыть диалог после успешного обновления
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось обновить данные: {str(e)}")
