from PyQt5.QtWidgets import QHeaderView, QHBoxLayout, QApplication, QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
import psycopg2
from PyQt5.QtCore import Qt
from connection import ConnectionManager
from add_norm import AddNorm
from update_norm import UpdateNorm  

class Norms(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        super().__init__()
        self.conn: ConnectionManager = conn
        layout = QVBoxLayout(self)
        self.setWindowTitle("Нормы")
        self.setFixedSize(600, 400)
        
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        
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
        
        self.back_button = QPushButton("Вернуться на главное окно")
        self.back_button.clicked.connect(self.go_to_main_window)
        layout.addWidget(self.back_button)

        self.table_widget = QTableWidget()
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)  # Set selection mode
        layout.addWidget(self.table_widget)

        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        if not IsAdmin:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
            self.update_button.setEnabled(False)

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
                
        self.table_widget.resizeColumnsToContents()

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
