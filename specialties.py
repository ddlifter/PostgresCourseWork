from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
from connection import ConnectionManager
from add_specialty import AddSpecialty
from update_specialty import UpdateSpecialty
from PyQt5.QtCore import Qt

class Specialties(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        self.conn : ConnectionManager = conn
        super().__init__()
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Специальности")
        self.setGeometry(100, 100, 600, 400)
        self.setLayout(layout)
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)  # Установите размеры и позицию

        # Set the selection behavior to select entire rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.show_data_button = QPushButton("Показать данные")
        self.show_data_button.clicked.connect(self.load_data_from_db)
        layout.addWidget(self.show_data_button)
        
        self.update_data_button = QPushButton("Обновить данные")
        self.update_data_button.clicked.connect(self.open_update_dialog)
        layout.addWidget(self.update_data_button)
        
        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_selected_row)
        layout.addWidget(self.delete_button)
        
        self.back_button = QPushButton("Вернуться на главное окно")  # Создаем кнопку
        self.back_button.clicked.connect(self.go_to_main_window)  # Подключаем метод
        layout.addWidget(self.back_button)
        
        layout.addWidget(self.table_widget)
        
        if not IsAdmin:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.update_data_button.setEnabled(False)
            self.show_data_button.setEnabled(False)

        # Load data from database and configure table
        self.load_data_from_db()
        
    def go_to_main_window(self):
        self.main_form.show()
        self.close()

    def load_data_from_db(self):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.callproc('select_specialties')
                rows = cur.fetchall()
                
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0]) - 1)  # Уменьшаем количество столбцов на 1
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row[1:]):  # Начинаем с первого элемента, чтобы пропустить id
                item = QTableWidgetItem(str(value))
                # Make cells read-only
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

    def open_add_dialog(self):
        dialog = AddSpecialty(self.conn)
        if dialog.exec_():
            self.load_data_from_db()
            
    def delete_selected_row(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                selected_rows = self.table_widget.selectionModel().selectedRows()
                if not selected_rows:
                    QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
                    return
                # Определяем id по другим полям (например, по названию специальности)
                spec_name = self.table_widget.item(selected_rows[0].row(), 0).text()
                try:
                    cursor.execute("DELETE FROM specialties WHERE name = %s", (spec_name,))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Строка успешно удалена.")
                    self.load_data_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить строку: {str(e)}")
                    
    def open_update_dialog(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Напоминание", "Выберите строку для обновления.")
            return

        selected_row_index = selected_rows[0].row()
        spec_name = self.table_widget.item(selected_row_index, 0).text()
        description = self.table_widget.item(selected_row_index, 1).text()
        
        # Запрос id_specialty из базы данных по name и description
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_specialty FROM specialties WHERE name = %s AND description = %s", (spec_name, description))
                id_specialty = cur.fetchone()[0]  # Получаем первый элемент первой строки (предполагается, что будет только одна строка)

        dialog = UpdateSpecialty(self.conn, id_specialty, spec_name, description)  # Передаем id_specialty в UpdateSpecialty
        if dialog.exec_():
            self.load_data_from_db()
