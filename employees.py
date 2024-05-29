from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
import psycopg2
from PyQt5.QtCore import Qt
from connection import ConnectionManager
from add_employee import AddEmployee
from update_employee import UpdateEmployee  # Подключаем класс для окна обновления сотрудника

class Employees(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        super().__init__()
        self.conn: ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Сотрудники")
        self.setGeometry(100, 100, 600, 400)
        self.setLayout(layout)
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)

        # Set the selection behavior to select entire rows
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_button = QPushButton("Добавить сотрудника")
        self.add_button.clicked.connect(self.open_add_dialog)
        layout.addWidget(self.add_button)

        self.show_data_button = QPushButton("Показать данные")
        self.show_data_button.clicked.connect(self.load_data_from_db)
        layout.addWidget(self.show_data_button)

        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.open_update_dialog)
        layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_selected_row)
        layout.addWidget(self.delete_button)
        
        self.back_button = QPushButton("Вернуться на главное окно")  # Создаем кнопку
        self.back_button.clicked.connect(self.go_to_main_window)  # Подключаем метод
        layout.addWidget(self.back_button)  # Добавляем кнопку в макет

        layout.addWidget(self.table_widget)

        if not IsAdmin:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.update_button.setEnabled(False)
            self.show_data_button.setEnabled(False)

        self.load_data_from_db()
        
        
    def go_to_main_window(self):
        self.main_form.show()
        self.close()
        
        

    def load_data_from_db(self):
        query = """
            SELECT employees.surname, employees.name, specialties.name AS specialty, specialties.description
            FROM employees
            LEFT JOIN specialties ON employees.id_specialty = specialties.id_specialty
        """
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

        if not rows:
            self.table_widget.hide()
            return

        self.table_widget.show()
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0]))
        column_names = ["Фамилия", "Имя", "Специальность", "Описание специальности"]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

    def open_add_dialog(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM specialties")
                count = cursor.fetchone()[0]

                if count == 0:
                    QMessageBox.warning(self, "Нет специальностей", "В таблице Специальности нет записей, сперва добавьте информацию о специальностях.")
                else:
                    dialog = AddEmployee(self.conn)
                    if dialog.exec_():
                        self.load_data_from_db()


    def delete_selected_row(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                selected_indexes = self.table_widget.selectionModel().selectedRows()
                if not selected_indexes:
                    QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
                    return

                index = selected_indexes[0]
                surname = self.table_widget.item(index.row(), 0).text()
                name = self.table_widget.item(index.row(), 1).text()
                try:
                    cursor.execute("DELETE FROM employees WHERE surname = %s AND name = %s", (surname, name))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Строка успешно удалена.")
                    self.load_data_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить строку: {str(e)}")

    def open_update_dialog(self):
        selected_indexes = self.table_widget.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, "Уведомление", "Выберите строку для обновления.")
            return

        selected_row_index = selected_indexes[0].row()
        surname = self.table_widget.item(selected_row_index, 0).text()
        name = self.table_widget.item(selected_row_index, 1).text()

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_employee FROM employees WHERE surname = %s AND name = %s", (surname, name))
                id_employee = cur.fetchone()[0]

        dialog = UpdateEmployee(self.conn, id_employee, surname, name)
        if dialog.exec_():
            self.load_data_from_db()
