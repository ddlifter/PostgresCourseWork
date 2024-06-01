from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QHBoxLayout, QSizePolicy
from employees import Employees
from specialties import Specialties
from norms import Norms
from ranks import Ranks
from training import Training
import sys
from connection import ConnectionManager
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QFont
import psycopg2

IsAdmin = True

class MainForm(QMainWindow):
    def __init__(self, conn: ConnectionManager, IsAdmin):
        self.conn : ConnectionManager = conn
        super().__init__()
        self.setWindowTitle("Главное меню")
        self.setFixedSize(480, 280)
        
        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

        main_layout = QVBoxLayout()

        training_layout = QHBoxLayout()
        self.training_button = QPushButton("Процесс обучения")
        self.training_button.clicked.connect(self.open_training_form)
        self.training_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        training_layout.addWidget(self.training_button)
        main_layout.addLayout(training_layout)

        main_layout.addWidget(QWidget())  
        label = QLabel("Справочники")
        label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(label)

        references_layout = QHBoxLayout()
        buttons_info = [("Сотрудники", self.open_form1),
                        ("Специальности", self.open_form2)]
        for text, function in buttons_info:
            button = QPushButton(text)
            button.clicked.connect(function)
            references_layout.addWidget(button)
        main_layout.addLayout(references_layout)

        # Создаем layout для кнопок "Нормы" и "Разряды"
        norms_layout = QHBoxLayout()
        buttons_info = [("Нормы", self.open_form3),
                        ("Разряды", self.open_form4)]
        for text, function in buttons_info:
            button = QPushButton(text)
            button.clicked.connect(function)
            norms_layout.addWidget(button)
        main_layout.addLayout(norms_layout)

        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.open_login_form)
        main_layout.addWidget(self.logout_button, alignment=Qt.AlignCenter)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)


    def open_training_form(self):
        self.training_form = Training(self, self.conn, IsAdmin)
        self.training_form.show()
        self.close()

    def open_form1(self):
        self.form1 = Employees(self, self.conn, IsAdmin)
        self.form1.show()
        self.close()

    def open_form2(self):
        self.form2 = Specialties(self, self.conn, IsAdmin)
        self.form2.show()
        self.close()

    def open_form3(self):
        self.form3 = Norms(self, self.conn, IsAdmin)
        self.form3.show()
        self.close()

    def open_form4(self):
        self.form4 = Ranks(self, self.conn, IsAdmin)
        self.form4.show()
        self.close()

    def open_login_form(self):
        self.login_form = AuthorizationWindow()
        self.login_form.show()
        self.close()
class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Авторизация")
        self.setFixedSize(400, 200)

        screen_geometry = QApplication.desktop().availableGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)


        layout = QVBoxLayout()

        username_layout = QHBoxLayout()
        username_layout.setAlignment(Qt.AlignCenter)
        self.usernameLabel = QLabel("Логин:", self)
        self.usernameInput = QLineEdit(self)
        username_layout.addWidget(self.usernameLabel)
        username_layout.addWidget(self.usernameInput)
        layout.addLayout(username_layout)

        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignCenter)
        self.passwordLabel = QLabel("Пароль:", self)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.passwordLabel)
        password_layout.addWidget(self.passwordInput)
        layout.addLayout(password_layout)

        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)
        self.loginButton = QPushButton("Войти", self)
        self.loginButton.clicked.connect(self.handleLogin)
        button_layout.addWidget(self.loginButton)
        layout.addLayout(button_layout)

        self.setLayout(layout)


    def handleLogin(self):
        global IsAdmin
        username = self.usernameInput.text()
        password = self.passwordInput.text()
        
        if username == "admin" and password == "12345":
            role = "admin_role"
            IsAdmin = True
        else:
            conn = psycopg2.connect(host='localhost', user='postgres', password='12345', database='postgres')
            cursor = conn.cursor()
            
            cursor.execute("SELECT surname FROM employees")
            employee_surnames = [row[0] for row in cursor.fetchall()]  # Получаем все фамилии сотрудников в массив

            if username in employee_surnames and password == "12345":
                role = "employee_user"
                IsAdmin = False
            else:
                QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")
                return
            
            cursor.close()
            conn.close()

        conn = ConnectionManager(role)
        self.form1 = MainForm(conn, IsAdmin)
        self.form1.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = AuthorizationWindow()
    main_form.show()
    sys.exit(app.exec_())
