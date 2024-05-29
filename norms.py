from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem
import psycopg2

from connection import ConnectionManager
from add_norm import AddNorm
from update_norm import UpdateNorm  # Подключаем класс для окна обновления сотрудника

class Norms(QWidget):
    def __init__(self, conn: ConnectionManager, IsAdmin):
        super().__init__()
        self.conn: ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Нормы")
        self.setGeometry(100, 100, 600, 400)
        self.setLayout(layout)
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)
        
        self.add_button = QPushButton("Добавить")
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
        
        layout.addWidget(self.table_widget)

        if IsAdmin != True:
            self.add_button.setEnabled(False)
            self.delete_button.setEnabled(False)
        

    def load_data_from_db(self):
        query = """
            SELECT norms.name, norms.description, ranks.name AS rank, ranks.description
            FROM norms
            INNER JOIN ranks ON norms.id_rank = ranks.id_rank
        """
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(query)
                rows = cur.fetchall()

        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0]))

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(value)))


    def open_add_dialog(self):
        dialog = AddNorm(self.conn)
        if dialog.exec_():
            self.load_data_from_db()
            
    
    def delete_selected_row(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                selected_indexes = self.table_widget.selectionModel().selectedRows()
                if not selected_indexes:
                    QMessageBox.information(self, "Уведомление", "Выебрите строку для удаления.")
                    return

                index = selected_indexes[0]
                surname = self.table_widget.item(index.row(), 0).text()
                name = self.table_widget.item(index.row(), 1).text()
                try:
                    cursor.execute("DELETE FROM norms WHERE name = %s AND description = %s", (surname, name))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Строка успешно удалена.")
                    self.load_data_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to delete row: {str(e)}")

                    
    def open_update_dialog(self):
        selected_indexes = self.table_widget.selectionModel().selectedRows()
        if not selected_indexes:
            QMessageBox.information(self, "Reminder", "Select a row to update.")
            return

        selected_row_index = selected_indexes[0].row()
        surname = self.table_widget.item(selected_row_index, 0).text()
        name = self.table_widget.item(selected_row_index, 1).text()
        
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_norm FROM norms WHERE name = %s AND description = %s", (surname, name))
                id_employee = cur.fetchone()[0]

        dialog = UpdateNorm(self.conn, id_employee, surname, name)
        if dialog.exec_():
            self.load_data_from_db()
