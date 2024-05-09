from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QWidget, QLabel, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem
import psycopg2

from connection import ConnectionManager
from add_norm import AddNorm

class Norms(QWidget):
    def __init__(self, conn: ConnectionManager, IsAdmin) :
        self.conn : ConnectionManager = conn
        super().__init__()
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Нормы")
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
                cursor.execute("SELECT * FROM norms")  # Убедитесь, что имя таблицы верно
                rows = cursor.fetchall()
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
                selected_rows = self.table_widget.selectionModel().selectedRows()
                if not selected_rows:
                    QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
                    return
                norm_id = self.table_widget.item(selected_rows[0].row(), 0).text()  # Предполагается, что ID сотрудника находится в первом столбце
                try:
                    cursor.execute("DELETE FROM norms WHERE id_norm = %s", (norm_id,))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Строка успешно удалена.")
                    self.load_data_from_db()
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить строку: {str(e)}")

