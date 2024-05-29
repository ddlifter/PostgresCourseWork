from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGridLayout, QWidget, QLabel, QVBoxLayout, QLineEdit, QMessageBox
from employees import Employees
from specialties import Specialties
from norms import Norms
from ranks import Ranks
from training import Training
import sys
from connection import ConnectionManager
from PyQt5.QtCore import Qt  


IsAdmin = True

class MainForm(QMainWindow):
    def __init__(self, conn: ConnectionManager, IsAdmin):
        self.conn : ConnectionManager = conn
        super().__init__()
        self.setWindowTitle("Main Form")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()

        # Создаем сетку для размещения кнопок
        grid_layout = QGridLayout()

        # Кнопка Обучение в центре
        self.training_button = QPushButton("Обучение (основная)")
        self.training_button.clicked.connect(self.open_training_form)
        self.training_label = QLabel("При нажатии переходит к редактированию обучений.")
        grid_layout.addWidget(self.training_label, 0, 0, alignment=Qt.AlignCenter)
        grid_layout.addWidget(self.training_button, 0, 1, alignment=Qt.AlignCenter)

        # Остальные кнопки внизу
        self.button1 = QPushButton("Сотрудники")
        self.button1.clicked.connect(self.open_form1)
        grid_layout.addWidget(self.button1, 1, 0)

        self.button2 = QPushButton("Специальности")
        self.button2.clicked.connect(self.open_form2)
        grid_layout.addWidget(self.button2, 1, 1)

        self.button3 = QPushButton("Нормы")
        self.button3.clicked.connect(self.open_form3)
        grid_layout.addWidget(self.button3, 1, 2)

        self.button4 = QPushButton("Разряды")
        self.button4.clicked.connect(self.open_form4)
        grid_layout.addWidget(self.button4, 2, 0)

        # Добавляем кнопку "Выйти"
        self.logout_button = QPushButton("Выйти")
        self.logout_button.clicked.connect(self.open_login_form)  # Подключаем метод для открытия окна авторизации
        grid_layout.addWidget(self.logout_button, 2, 1)

        # Устанавливаем сетку в качестве центрального виджета
        central_widget = QWidget()
        central_widget.setLayout(grid_layout)
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
        # Открываем окно авторизации
        self.login_form = AuthorizationWindow()
        self.login_form.show()
        self.close()

class AuthorizationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Авторизация")
        self.setGeometry(300, 300, 400, 200)

        layout = QVBoxLayout()

        self.usernameLabel = QLabel("Логин:")
        layout.addWidget(self.usernameLabel)
        self.usernameInput = QLineEdit()
        layout.addWidget(self.usernameInput)

        self.passwordLabel = QLabel("Пароль:")
        layout.addWidget(self.passwordLabel)
        self.passwordInput = QLineEdit()
        self.passwordInput.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.passwordInput)

        self.loginButton = QPushButton("Войти")
        self.loginButton.clicked.connect(self.handleLogin)
        layout.addWidget(self.loginButton)

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
