from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QHeaderView, QLineEdit, QDialog, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
import psycopg2
from PyQt5.QtCore import Qt
from connection import ConnectionManager
from add_training import AddTraining
from update_training import UpdateTraining

class Training(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        super().__init__()
        self.conn: ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Обучение")
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
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        layout.addWidget(self.table_widget)

        self.setLayout(layout)

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
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT e.surname, n.name, t.data FROM training t JOIN employees e ON t.id_employee = e.id_employee JOIN norms n ON t.id_norm = n.id_norm")
                rows = cur.fetchall()

        self.table_widget.clear()  

        if not rows:
            self.table_widget.hide()
            return

        self.table_widget.show()
        self.table_widget.setRowCount(len(rows))
        self.table_widget.setColumnCount(len(rows[0]))
        column_names = ["Сотрудник", "Норма", "Дата"]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)  
                self.table_widget.setItem(i, j, item)
                
        self.table_widget.resizeColumnsToContents()

    def open_add_dialog(self):
        dialog = AddTraining(self.conn)
        if dialog.exec_():
            self.load_data_from_db()
            
    def open_update_dialog(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Напоминание", "Выберите строку для обновления.")
            return

        selected_row_index = selected_rows[0].row()
        surname = self.table_widget.item(selected_row_index, 0).text()
        norm = self.table_widget.item(selected_row_index, 1).text()
        date = self.table_widget.item(selected_row_index, 2).text()

        with self.conn as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute("SELECT id_training FROM training WHERE id_employee IN (SELECT id_employee FROM employees WHERE surname = %s) AND id_norm IN (SELECT id_norm FROM norms WHERE name = %s) AND data = %s", (surname, norm, date))
                    training_id = cur.fetchone()[0]
                except Exception as e:
                    print(f"Ошибка при получении id_training: {e}")
                    return

        dialog = UpdateTraining(self.conn, training_id)
        if dialog.exec_():
            self.load_data_from_db()

    def delete_selected_row(self):
        selected_rows = self.table_widget.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.information(self, "Уведомление", "Выберите строку для удаления.")
            return

        selected_row_index = selected_rows[0].row()
        surname_item = self.table_widget.item(selected_row_index, 0)
        norm_item = self.table_widget.item(selected_row_index, 1)
        date_item = self.table_widget.item(selected_row_index, 2)

        if not all([surname_item, norm_item, date_item]):
            return  # Если выбранные элементы ячеек пусты, просто выходим

        surname = surname_item.text()
        norm = norm_item.text()
        date = date_item.text()

        with self.conn as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute("DELETE FROM training WHERE id_employee IN (SELECT id_employee FROM employees WHERE surname = %s) AND id_norm IN (SELECT id_norm FROM norms WHERE name = %s) AND data = %s", (surname, norm, date))
                    conn.commit()
                    QMessageBox.information(self, "Успех", "Строка успешно удалена.")
                    
                    self.load_data_from_db()
                     
                except Exception as e:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось удалить строку: {str(e)}")
