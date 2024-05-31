from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QMessageBox, QHBoxLayout
from employees import Employees
from specialties import Specialties
from norms import Norms
from ranks import Ranks
from training import Training
import sys
from connection import ConnectionManager
from PyQt5.QtCore import Qt 
from PyQt5.QtGui import QFont

IsAdmin = True

class MainForm(QMainWindow):
    def __init__(self, conn: ConnectionManager, IsAdmin):
        self.conn : ConnectionManager = conn
        super().__init__()
        self.setWindowTitle("Главное меню")
        self.setGeometry(100, 100, 600, 400)

        # Создаем вертикальный layout для размещения кнопок
        layout = QVBoxLayout()

        # Кнопка "Обучение" - акцентированная
        self.training_button = QPushButton("Обучение (основная)")
        self.training_button.clicked.connect(self.open_training_form)
        self.training_button.setStyleSheet("background-color: #4CAF50; color: white; border: none; padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer;")
        layout.addWidget(self.training_button)

        # Кнопка "Выйти" рядом с кнопкой "Обучение"
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.open_login_form)
        layout.addWidget(self.logout_button)

        # Отдельный блок для остальных кнопок
        other_buttons_layout = QVBoxLayout()

        # Кнопки для различных форм
        buttons_info = [("Сотрудники", self.open_form1),
                        ("Специальности", self.open_form2),
                        ("Нормы", self.open_form3),
                        ("Разряды", self.open_form4)]
        for text, function in buttons_info:
            button = QPushButton(text)
            button.clicked.connect(function)
            other_buttons_layout.addWidget(button)

        # Добавляем блок с остальными кнопками в основной layout
        layout.addLayout(other_buttons_layout)

        # Устанавливаем layout в качестве центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(layout)
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

        # Макет для поля ввода логина
        username_layout = QHBoxLayout()
        username_layout.setAlignment(Qt.AlignCenter)
        self.usernameLabel = QLabel("Логин:", self)
        self.usernameInput = QLineEdit(self)
        username_layout.addWidget(self.usernameLabel)
        username_layout.addWidget(self.usernameInput)
        layout.addLayout(username_layout)

        # Макет для поля ввода пароля
        password_layout = QHBoxLayout()
        password_layout.setAlignment(Qt.AlignCenter)
        self.passwordLabel = QLabel("Пароль:", self)
        self.passwordInput = QLineEdit(self)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.passwordLabel)
        password_layout.addWidget(self.passwordInput)
        layout.addLayout(password_layout)

        # Макет для кнопки
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
        elif username == "employee" and password == "12345":
            role = "employee_user"
            IsAdmin = False
        else:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль.")
            return

        conn = ConnectionManager(role)
        self.form1 = MainForm(conn, IsAdmin)
        self.form1.show()
        self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_form = AuthorizationWindow()
    main_form.show()
    sys.exit(app.exec_())
