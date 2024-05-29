from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
import psycopg2
from PyQt5.QtCore import Qt
from connection import ConnectionManager
from add_norm import AddNorm
from update_norm import UpdateNorm  # Подключаем класс для окна обновления сотрудника

class Norms(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        super().__init__()
        self.conn: ConnectionManager = conn
        layout = QVBoxLayout(self)
        self.setWindowTitle("Нормы")
        self.setGeometry(100, 100, 600, 400)
        

        # Создаем вертикальный layout для кнопок
        button_layout = QVBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.open_add_dialog)
        button_layout.addWidget(self.add_button)

        self.show_data_button = QPushButton("Показать данные")
        self.show_data_button.clicked.connect(self.load_data_from_db)
        button_layout.addWidget(self.show_data_button)

        self.update_button = QPushButton("Обновить")
        self.update_button.clicked.connect(self.open_update_dialog)
        button_layout.addWidget(self.update_button)

        self.delete_button = QPushButton("Удалить")
        self.delete_button.clicked.connect(self.delete_selected_row)
        button_layout.addWidget(self.delete_button)
        
        self.back_button = QPushButton("Вернуться на главное окно")  # Создаем кнопку
        self.back_button.clicked.connect(self.go_to_main_window)  # Подключаем метод
        button_layout.addWidget(self.back_button)

        layout.addLayout(button_layout)

        # Создаем виджет таблицы и настраиваем его
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.table_widget)

        if not IsAdmin:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.update_button.setEnabled(False)
            self.show_data_button.setEnabled(False)

        # Загружаем данные из базы данных и настраиваем таблицу
        self.load_data_from_db()
        
    def go_to_main_window(self):
        self.main_form.show()
        self.close()

    def load_data_from_db(self):
        query = """
            SELECT norms.name, norms.description, ranks.name AS rank, ranks.description
            FROM norms
            LEFT JOIN ranks ON norms.id_rank = ranks.id_rank
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
        column_names = ["Норма", "Описание нормы", "Разряд", "Описание разряда"]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)

    def open_add_dialog(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT COUNT(*) FROM ranks")
                count = cursor.fetchone()[0]

                if count == 0:
                    QMessageBox.warning(self, "Нет разрядов", "В таблице Разряды нет записей, сперва добавьте информацию о разрядах.")
                else:
                    dialog = AddNorm(self.conn)
                    if dialog.exec_():
                        self.load_data_from_db()

    def delete_selected_row(self):
        selected_indexes = self.table_widget.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
            return

        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM norms WHERE name = %s AND description = %s", (self.table_widget.item(selected_indexes[0].row(), 0).text(), self.table_widget.item(selected_indexes[0].row(), 1).text()))
                conn.commit()

        self.load_data_from_db()

    def open_update_dialog(self):
        selected_indexes = self.table_widget.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, "Напоминание", "Выберите строку для обновления.")
            return

        selected_row_index = selected_indexes[0].row()
        surname = self.table_widget.item(selected_row_index, 0).text()
        name = self.table_widget.item(selected_row_index, 1).text()

        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_norm FROM norms WHERE name = %s AND description = %s", (surname, name))
                id_norm = cur.fetchone()[0]

        dialog = UpdateNorm(self.conn, id_norm, surname, name)
        if dialog.exec_():
            self.load_data_from_db()
