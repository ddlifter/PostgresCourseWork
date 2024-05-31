from PyQt5.QtWidgets import QApplication, QHBoxLayout, QHeaderView, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
from connection import ConnectionManager
from PyQt5.QtCore import Qt
from add_rank import AddRank
from update_rank import UpdateRank  # Подключаем класс для окна обновления разряда

class Ranks(QWidget):
    def __init__(self, main_form, conn: ConnectionManager, IsAdmin):
        self.main_form = main_form
        super().__init__()
        self.conn: ConnectionManager = conn
        self.showMaximized()
        layout = QVBoxLayout()
        self.setWindowTitle("Разряды")
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
            SELECT name, description FROM ranks
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
        column_names = ["Разряд", "Описание разряда"]
        self.table_widget.setHorizontalHeaderLabels(column_names)

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ Qt.ItemIsEditable)
                self.table_widget.setItem(i, j, item)
                
        self.table_widget.resizeColumnsToContents()

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
                rank_name = self.table_widget.item(selected_rows[0].row(), 0).text()
                description = self.table_widget.item(selected_rows[0].row(), 1).text()
                try:
                    cursor.execute("DELETE FROM ranks WHERE name = %s AND description = %s", (rank_name, description))
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
        
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id_rank FROM ranks WHERE name = %s AND description = %s", (rank_name, description))
                id_rank = cur.fetchone()[0]

        dialog = UpdateRank(self.conn, id_rank, rank_name, description)
        if dialog.exec_():
            self.load_data_from_db()
