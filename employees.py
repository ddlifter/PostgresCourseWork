from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QHeaderView, QHBoxLayout, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView, QApplication
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
        self.setFixedSize(600, 400)
        
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
        # Создаем горизонтальный layout для кнопок "Добавить", "Изменить", "Удалить"
        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)
        button_layout.addWidget(self.add_button)

        self.update_button = QPushButton("Изменить")
        self.update_button.clicked.connect(self.open_update_dialog)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_selected_row)
        button_layout.addWidget(self.delete_button)
        
        layout.addLayout(button_layout)
        
        # Создаем кнопку для возврата на главное окно
        self.back_button = QPushButton("Вернуться на главное окно")
        self.back_button.clicked.connect(self.go_to_main_window)
        layout.addWidget(self.back_button)

        # Создаем виджет таблицы и настраиваем его
        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        if not IsAdmin:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.update_button.setEnabled(False)

        # Загружаем данные из базы данных и настраиваем таблицу
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
        column_names = ["Фамилия", "Имя", "Специальность", "Описание"]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)
                
        self.table_widget.resizeColumnsToContents()

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
