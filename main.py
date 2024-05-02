import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QListWidget
import psycopg2

class DatabaseForm(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("PostgreSQL Tables Viewer")
        
        self.connect_button = QPushButton("Connect to Database")
        self.connect_button.clicked.connect(self.connect_to_database)
        
        self.table_list = QListWidget()
        
        layout = QVBoxLayout()
        layout.addWidget(self.connect_button)
        layout.addWidget(self.table_list)
        
        self.setLayout(layout)
    
    def connect_to_database(self):
        try:
            conn = psycopg2.connect(
                dbname="postgres",
                user="postgres",
                password="12345",
                host="localhost"
            )
            cur = conn.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
            tables = cur.fetchall()
            self.table_list.clear()
            for table in tables:
                self.table_list.addItem(table[0])
            conn.close()
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = DatabaseForm()
    form.show()
    sys.exit(app.exec_())
