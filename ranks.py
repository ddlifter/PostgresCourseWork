from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox
from connection import ConnectionManager
from add_rank import AddRank
from update_rank import UpdateRank  # Подключаем класс для окна обновления разряда

class Ranks(QWidget):
    def __init__(self, conn: ConnectionManager, IsAdmin):
        super().__init__()
        self.conn : ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Разряды")
        self.setGeometry(100, 100, 600, 400)
        self.setLayout(layout)
        self.table_widget = QTableWidget()
        self.table_widget.setGeometry(50, 50, 500, 300)  # Установите размеры и позицию
        
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
        with self.conn as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT name, description FROM ranks")
                rows = cursor.fetchall()
                self.table_widget.setRowCount(len(rows))
                self.table_widget.setColumnCount(len(rows[0]))
                for i, row in enumerate(rows):
                    for j, value in enumerate(row):
                        self.table_widget.setItem(i, j, QTableWidgetItem(str(value)))

    def open_add_dialog(self):
        dialog = AddRank(self.conn)
        if dialog.exec_():
            self.load_data_from_db()
            
    def delete_selected_row(self):
        with self.conn as conn:
            with conn.cursor() as cursor:
                selected_rows = self.table_widget.selectionModel().selectedRows()
                if not selected_rows:
                    QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
                    return
                # Определяем id по другим полям (например, по названию разряда)
                rank_name = self.table_widget.item(selected_rows[0].row(), 1).text()
                description = self.table_widget.item(selected_rows[0].row(), 2).text()
                try:
                    cursor.execute("DELETE FROM ranks WHERE rank_name = %s AND description = %s", (rank_name, description))
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
        rank_name = self.table_widget.item(selected_row_index, 0).text()
        description = self.table_widget.item(selected_row_index, 1).text()
        
        # Запрос id_rank из базы данных по name и description
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_rank FROM ranks WHERE name = %s AND description = %s", (rank_name, description))
                id_rank = cur.fetchone()[0]  # Получаем первый элемент первой строки (предполагается, что будет только одна строка)

        dialog = UpdateRank(self.conn, id_rank, rank_name, description)  # Передаем id_rank в UpdateRank
        if dialog.exec_():
            self.load_data_from_db()
